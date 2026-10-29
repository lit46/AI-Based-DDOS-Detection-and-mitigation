#!/usr/bin/env python3
"""
Locked topology for the recapture. Strict role separation:
  - h1, h2, h3: NORMAL only. Never run hping3.
  - h4, h5: ATTACKER only. Never run legitimate traffic (ping/iperf/curl).
  - h6: BROWSER only, NAT'd to real internet.

    Floodlight (remote controller)
        |
       s1 --- root (NAT -> real internet)
      /  \
    s2    s3
   /|\     |\
  h1 h2 h3 h4 h5      h6 (attached directly to s1)
 (NORMAL)  (ATTACKER) (BROWSER)

IMPORTANT: confirm INET_INTF below matches your real interface
(`ip -br addr`) -- already set to wlp2s0 per your last confirmed setup.
"""

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch, Node
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

INET_INTF = 'wlp2s0'  # confirmed via `ip -br addr` last session


def start_nat(root, inet_intf=INET_INTF, subnet='10.0.0.0/24'):
    local_intf = root.defaultIntf()

    root.cmd('iptables -F')
    root.cmd('iptables -t nat -F')
    root.cmd('iptables -P INPUT ACCEPT')
    root.cmd('iptables -P OUTPUT ACCEPT')
    root.cmd('iptables -P FORWARD DROP')

    root.cmd(f'iptables -I FORWARD -i {local_intf} -d {subnet} -j DROP')
    root.cmd(f'iptables -A FORWARD -i {local_intf} -s {subnet} -j ACCEPT')
    root.cmd(f'iptables -A FORWARD -i {inet_intf} -d {subnet} -j ACCEPT')
    root.cmd(f'iptables -t nat -A POSTROUTING -o {inet_intf} -j MASQUERADE')

    root.cmd('sysctl -w net.ipv4.ip_forward=1')


def build():
    net = Mininet(controller=RemoteController, switch=OVSSwitch, link=TCLink, autoSetMacs=True)

    info('*** Adding controller\n')
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)

    info('*** Adding switches\n')
    s1 = net.addSwitch('s1', protocols='OpenFlow13')
    s2 = net.addSwitch('s2', protocols='OpenFlow13')
    s3 = net.addSwitch('s3', protocols='OpenFlow13')

    info('*** Adding hosts\n')
    # NORMAL cluster -- legitimate traffic only, never hping3
    h1 = net.addHost('h1', ip='10.0.0.1/24')
    h2 = net.addHost('h2', ip='10.0.0.2/24')
    h3 = net.addHost('h3', ip='10.0.0.3/24')
    # ATTACKER cluster -- hping3 only, never legitimate traffic
    h4 = net.addHost('h4', ip='10.0.0.4/24')
    h5 = net.addHost('h5', ip='10.0.0.5/24')
    # BROWSER host -- NAT'd, real internet only
    h6 = net.addHost('h6', ip='10.0.0.6/24')

    info('*** Creating links\n')
    net.addLink(s1, s2)
    net.addLink(s1, s3)
    net.addLink(s2, h1, bw=10)
    net.addLink(s2, h2, bw=10)
    net.addLink(s2, h3, bw=10)
    net.addLink(s3, h4, bw=10)
    net.addLink(s3, h5, bw=10)
    net.addLink(s1, h6, bw=10)

    info('*** Adding NAT root node for internet access\n')
    root = Node('root', inNamespace=False)
    root_intf = net.addLink(root, s1).intf1
    root.setIP('10.0.0.254', prefixLen=24, intf=root_intf)

    net.build()
    c0.start()
    for sw in (s1, s2, s3):
        sw.start([c0])

    info('*** Configuring NAT/forwarding\n')
    start_nat(root, inet_intf=INET_INTF, subnet='10.0.0.0/24')

    # only h6 needs internet routing/DNS -- but harmless to set on all,
    # keeps things simple and consistent
    for host in (h1, h2, h3, h4, h5, h6):
        host.cmd('ip route add default via 10.0.0.254')
        host.cmd('echo "nameserver 8.8.8.8" > /etc/resolv.conf')

    info('*** Network built. Waiting 3s for switches to settle before CLI...\n')
    import time
    time.sleep(3)

    info('*** Network ready. Dropping to CLI.\n')
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    build()
