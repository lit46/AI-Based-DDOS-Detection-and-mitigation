#!/usr/bin/env python3
"""
topo_loop.py -- same lab topology as topo_full.py, plus (1) attacker isolation, (2) a scripted labelled scenario for the closed loop.
  h1,h2,h3 NORMAL (h1 also runs a tiny web server)   h4,h5 ATTACKERS (hping3 -> h1 only)   h6 browser (idle in scenarios)
SAFETY: NAT rules drop everything sourced from 10.0.0.4/10.0.0.5 so attack traffic cannot leave the lab; the scenario refuses any
hping3 target outside 10.0.0.1-3. Run only on your own isolated machine.
  --scenario cli       build network and open the Mininet CLI (smoke test)
  --scenario collect   labelled rounds for training data
  --scenario loop      same rounds, for testing detector.py running in another terminal
"""
import argparse, csv, os, threading, time, urllib.request
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch, Node
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

INET_INTF = 'wlp2s0'
LAB_TARGETS = {"10.0.0.1", "10.0.0.2", "10.0.0.3"}
ATK = {"h4": "10.0.0.4", "h5": "10.0.0.5"}
# (attackers, hping3 inter-packet gap in microseconds): 500 / 1000 / 2000 packets per second
SYN_ROUNDS = [(("h4",), 2000, "syn"), (("h4", "h5"), 1000, "syn"), (("h5",), 500, "syn"), (("h4",), 1000, "syn"), (("h4", "h5"), 2000, "syn"), (("h5",), 1000, "syn")]
# variants the model was NOT trained on: other protocols, a low rate, and a legitimate flash crowd (no attacker at all)
VARIANTS = {
    "syn": SYN_ROUNDS,
    "udp": [(("h4",), 1000, "udp"), (("h4", "h5"), 1000, "udp"), (("h5",), 500, "udp")],
    "icmp": [(("h4",), 1000, "icmp"), (("h4", "h5"), 1000, "icmp"), (("h5",), 500, "icmp")],
    "lowrate": [(("h4",), 10000, "syn"), (("h5",), 10000, "syn"), (("h4", "h5"), 10000, "syn")],
    "flashcrowd": [((), 0, "flash")] * 4,
    # harder variants: attacks with full-size packets (1000-byte payload, 500 pps per attacker) ...
    "syn_big": [(("h4",), 2000, "synbig"), (("h4", "h5"), 2000, "synbig"), (("h5",), 2000, "synbig")],
    "udp_big": [(("h4",), 2000, "udpbig"), (("h4", "h5"), 2000, "udpbig"), (("h5",), 2000, "udpbig")],
    "icmp_big": [(("h4",), 2000, "icmpbig"), (("h4", "h5"), 2000, "icmpbig"), (("h5",), 2000, "icmpbig")],
    # ... and legitimate small-packet traffic (UDP, 12-byte payload, 30 packets/s from each of h2 and h3, like telemetry or voice)
    "smallpkt": [((), 33000, "small")] * 4,
    # heavy legitimate load: 12 parallel download loops from h2/h3 plus 200 pps small UDP, alone and under a full-size SYN flood
    "heavy": [((), 5000, "heavy")] * 3,
    "heavy_atk": [(("h4",), 2000, "heavyatk"), (("h4", "h5"), 2000, "heavyatk"), (("h5",), 2000, "heavyatk")],
}
HEAVY = ("flash", "heavy", "heavyatk")


def start_nat(root, inet_intf=INET_INTF, subnet='10.0.0.0/24'):
    local_intf = root.defaultIntf()
    root.cmd('iptables -F'); root.cmd('iptables -t nat -F')
    root.cmd('iptables -P INPUT ACCEPT'); root.cmd('iptables -P OUTPUT ACCEPT'); root.cmd('iptables -P FORWARD DROP')
    root.cmd(f'iptables -I FORWARD -i {local_intf} -d {subnet} -j DROP')
    root.cmd(f'iptables -A FORWARD -i {local_intf} -s {subnet} -j ACCEPT')
    root.cmd(f'iptables -A FORWARD -i {inet_intf} -d {subnet} -j ACCEPT')
    root.cmd(f'iptables -t nat -A POSTROUTING -o {inet_intf} -j MASQUERADE')
    root.cmd('sysctl -w net.ipv4.ip_forward=1')
    for ip in ATK.values():                       # attacker isolation: first rules in the chain
        root.cmd(f'iptables -I FORWARD 1 -s {ip} -j DROP')


def build():
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink, autoSetMacs=True)
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)
    s1, s2, s3 = [net.addSwitch(n, protocols='OpenFlow13') for n in ('s1', 's2', 's3')]
    hs = {f'h{i}': net.addHost(f'h{i}', ip=f'10.0.0.{i}/24') for i in range(1, 7)}
    net.addLink(s1, s2); net.addLink(s1, s3)
    for h, s in (('h1', s2), ('h2', s2), ('h3', s2), ('h4', s3), ('h5', s3), ('h6', s1)):
        net.addLink(s, hs[h], bw=10)
    root = Node('root', inNamespace=False)
    root_intf = net.addLink(root, s1).intf1
    root.setIP('10.0.0.254', prefixLen=24, intf=root_intf)
    net.build(); c0.start()
    for sw in (s1, s2, s3): sw.start([c0])
    start_nat(root)
    for h in hs.values():
        h.cmd('ip route add default via 10.0.0.254'); h.cmd('echo "nameserver 8.8.8.8" > /etc/resolv.conf')
    time.sleep(3)
    return net, hs


def clear_static(base):
    for ep in ("/wm/staticentrypusher/clear/all/json", "/wm/staticflowpusher/clear/all/json"):
        try:
            urllib.request.urlopen(base + ep, timeout=5).read(); return
        except Exception:
            continue


def scenario(net, hs, mode, rounds, out_dir, base, normal_s, attack_s, cool_s, variant='syn'):
    spec = VARIANTS[variant]
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs('/tmp/lab_www', exist_ok=True)
    open('/tmp/lab_www/index.html', 'w').write('lab\n')
    with open('/tmp/lab_www/big.bin', 'wb') as f: f.write(os.urandom(200_000))
    hs['h1'].cmd('python3 -m http.server 80 -d /tmp/lab_www >/dev/null 2>&1 &')
    hs['h2'].cmd('while true; do curl -s -o /dev/null http://10.0.0.1/big.bin; sleep 0.3; done >/dev/null 2>&1 &')
    hs['h3'].cmd('ping -i 0.2 10.0.0.1 >/dev/null 2>&1 &')
    stop = threading.Event()

    def monitor():                                 # packets arriving at the attack target, once per second
        with open(os.path.join(out_dir, 'traffic.csv'), 'w', newline='') as fh:
            w = csv.writer(fh); w.writerow(['t', 'rx_packets'])
            while not stop.is_set():
                v = hs['h1'].cmd("grep h1-eth0 /proc/net/dev | tr ':' ' ' | awk '{print $3}'").strip()
                w.writerow([round(time.time(), 3), v]); fh.flush(); time.sleep(1)
    threading.Thread(target=monitor, daemon=True).start()
    ev = open(os.path.join(out_dir, 'events.csv'), 'w', newline=''); ew = csv.writer(ev)
    ew.writerow(['t_start', 't_end', 'kind', 'attackers', 'pps', 'variant'])
    chk = open(os.path.join(out_dir, 'start_check.csv'), 'w', newline=''); cw = csv.writer(chk); cw.writerow(['round', 'host', 'tx_pps_measured', 'expected_pps', 'relaunched'])
    time.sleep(5)
    for r in range(rounds):
        atk, gap_us, proto = spec[r % len(spec)]
        info(f'*** round {r + 1}/{rounds} [{variant}]: normal {normal_s}s, {proto} {atk} for {attack_s}s\n')
        clear_static(base)
        time.sleep(normal_s)
        t0 = time.time()
        flag = {'syn': '-S -p 80', 'udp': '--udp -p 80', 'icmp': '--icmp', 'synbig': '-S -p 80 -d 1000', 'udpbig': '--udp -p 80 -d 1000', 'icmpbig': '--icmp -d 1000', 'heavyatk': '-S -p 80 -d 1000'}.get(proto)
        for h in atk:
            assert '10.0.0.1' in LAB_TARGETS
            hs[h].cmd(f'timeout {attack_s} hping3 {flag} -i u{gap_us} 10.0.0.1 >/dev/null 2>&1 &')
        if proto in HEAVY:                         # legitimate heavy load: parallel download loops from h2 and h3
            loops = '1 2 3 4' if proto == 'flash' else '1 2 3 4 5 6'
            for h in ('h2', 'h3'):
                hs[h].cmd(f'for i in {loops}; do timeout {attack_s} bash -c "while true; do curl -s -o /dev/null http://10.0.0.1/big.bin; done" >/dev/null 2>&1 & done')
            if proto != 'flash':                   # plus 200 pps of small legitimate UDP from each of h2 and h3
                for h in ('h2', 'h3'):
                    hs[h].cmd(f'timeout {attack_s} hping3 --udp -p 5004 -d 12 -i u5000 10.0.0.1 >/dev/null 2>&1 &')
        if atk:                                     # verify the flood really started; relaunch once if a host is silent
            def tx(h): return int((hs[h].cmd(f'cat /sys/class/net/{h}-eth0/statistics/tx_packets').strip() or '0'))
            before = {h: tx(h) for h in atk}; time.sleep(1.5)
            for h in atk:
                got = (tx(h) - before[h]) / 1.5; want = (1_000_000 // gap_us) if gap_us else 0; redo = want and got < 0.3 * want
                cw.writerow([r + 1, h, round(got, 1), want, int(bool(redo))]); chk.flush()
                if redo:
                    info(f'*** WARNING: {h} sent only {got:.0f} pps (wanted {want}) in {variant} round {r + 1}; relaunching hping3\n')
                    hs[h].cmd(f'timeout {max(2, attack_s - 2)} hping3 {flag} -i u{gap_us} 10.0.0.1 >/dev/null 2>&1 &')
        if proto == 'small':                       # legitimate small-packet application traffic
            for h in ('h2', 'h3'):
                hs[h].cmd(f'timeout {attack_s} hping3 --udp -p 5004 -d 12 -i u{gap_us} 10.0.0.1 >/dev/null 2>&1 &')
        time.sleep(attack_s - (1.5 if atk else 0))
        ew.writerow([round(t0, 3), round(time.time(), 3), 'flashcrowd' if proto in ('flash', 'heavy') else ('benign' if proto == 'small' else 'attack'),
                     '+'.join(ATK[h] for h in atk), (1_000_000 // gap_us) if gap_us else 0, variant]); ev.flush()
        time.sleep(cool_s)
    stop.set(); ev.close(); chk.close()
    info(f'*** done. Files in {out_dir}\n')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--scenario', default='cli', choices=['cli', 'collect', 'loop'])
    ap.add_argument('--rounds', type=int, default=6); ap.add_argument('--out_dir', default='loop_run')
    ap.add_argument('--base', default='http://127.0.0.1:8080')
    ap.add_argument('--normal_s', type=int, default=30); ap.add_argument('--attack_s', type=int, default=20)
    ap.add_argument('--cool_s', type=int, default=15)
    ap.add_argument('--variant', default='syn', choices=list(VARIANTS))
    a = ap.parse_args()
    setLogLevel('info')
    net, hs = build()
    if a.scenario == 'cli':
        CLI(net)
    else:
        scenario(net, hs, a.scenario, a.rounds, a.out_dir, a.base, a.normal_s, a.attack_s, a.cool_s, a.variant)
    net.stop()
