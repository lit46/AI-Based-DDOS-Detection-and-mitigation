#!/usr/bin/env python3
"""detector.py -- closed loop: poll Floodlight flow stats, score each source IP, install a drop rule when it looks like an attack.
Lab use only: it refuses to block 10.0.0.254 (the NAT/root node) and stops after --max_blocks blocks.
Logs: <log>_scores.csv (every score) and <log>_actions.csv (every block, with REST result)."""
import argparse, csv, json, os, signal, sys, time, urllib.request, urllib.error
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import loop_features as LF
from xgboost import XGBClassifier

ap = argparse.ArgumentParser()
ap.add_argument("--base", default="http://127.0.0.1:8080"); ap.add_argument("--model_dir", default="loop_model")
ap.add_argument("--log", default="detector"); ap.add_argument("--interval", type=float, default=1.0)
ap.add_argument("--consecutive", type=int, default=2, help="positive polls in a row before blocking")
ap.add_argument("--max_blocks", type=int, default=30, help="total rule installs before the detector stops blocking"); ap.add_argument("--duration", type=float, default=0)
ap.add_argument("--dry_run", action="store_true", help="score and log but never install rules")
ap.add_argument("--rule", default="", help="baseline mode: path to a rule json (one feature, one threshold) used instead of the XGB model")
ap.add_argument("--block_scope", choices=["all", "best"], default="all",
                help="all = drop rule on every switch that currently has an entry for the source (covers its ingress switch); best = only the switch with most traffic")
a = ap.parse_args()
signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt()))   # pkill leaves complete logs
if a.rule:
    rule = json.load(open(a.rule)); feats = [rule["feature"]]; idx = [LF.FEATS.index(rule["feature"])]; thr = 0.5; model = None
else:
    meta = json.load(open(os.path.join(a.model_dir, "loop_model_meta.json")))
    feats = meta["features"]; idx = [LF.FEATS.index(f) for f in feats]; thr = meta["threshold"]
    model = XGBClassifier(); model.load_model(os.path.join(a.model_dir, "loop_model.json"))
NEVER_BLOCK = {"10.0.0.254", "0.0.0.0"}
tr, hist, hits, recent, installs = LF.Tracker(), {}, {}, {}, 0
STALE_S = 20.0                          # history older than this is discarded (e.g. from a previous attack round)
endpoint = None

def call(path, body=None):
    req = urllib.request.Request(a.base + path, data=None if body is None else json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=5).read().decode()

def block(src, dpid):
    global endpoint
    body = {"switch": dpid, "name": "drop-" + src.replace(".", "-") + "-" + dpid.replace(":", ""), "priority": str(LF.DROP_PRIORITY),
            "eth_type": "0x0800", "ipv4_src": src, "active": "true"}      # no actions = drop
    for ep in ([endpoint] if endpoint else ["/wm/staticentrypusher/json", "/wm/staticflowpusher/json"]):
        try:
            r = call(ep, body); endpoint = ep; return True, r
        except urllib.error.HTTPError as e:
            if e.code != 404: return False, f"HTTP {e.code}"
        except Exception as e:
            return False, str(e)
    return False, "no static pusher endpoint found"

sc = open(a.log + "_scores.csv", "w", newline=""); ac = open(a.log + "_actions.csv", "w", newline="")
pc = open(a.log + "_polls.csv", "w", newline=""); pw = csv.writer(pc); pw.writerow(["t", "n_switches", "n_entries", "n_drop_rules", "drop_srcs", "poll_ms"]); pc.flush()
last_block = {}
sw, aw = csv.writer(sc), csv.writer(ac)
fc = open(a.log + "_feats.csv", "w", newline=""); fw = csv.writer(fc); fw.writerow(["t", "src", "dpid", "p_attack"] + LF.FEATS); fc.flush()
sw.writerow(["t", "src", "dpid", "p_attack"]); aw.writerow(["t_first_positive", "t_block", "src", "dpid", "ok", "reply", "secs_since_last_block", "n_switches_in_reply"]); ac.flush(); sc.flush()
first_pos = {}; t_end = time.time() + a.duration if a.duration else None
print("detector running (dry_run=%s) features=%s" % (a.dry_run, feats), flush=True)
try:
    while t_end is None or time.time() < t_end:
        t0 = time.time()
        try:
            obj = json.load(urllib.request.urlopen(a.base + "/wm/core/switch/all/flow/json", timeout=5))
        except Exception as e:
            print("poll failed:", e, flush=True); time.sleep(a.interval); continue
        if not isinstance(obj, dict) or len(obj) == 0:       # empty reply = switches momentarily gone; do not treat it as "no drop rules"
            pw.writerow([round(t0, 3), 0, 0, 0, "", round((time.time() - t0) * 1000)]); pc.flush()
            print("empty reply from Floodlight (no switches); skipping this poll", flush=True)
            time.sleep(max(0.0, a.interval - (time.time() - t0))); continue
        entries = LF.parse_flows(obj)
        sw_of = {}
        for e in entries:
            if e["prio"] < LF.DROP_PRIORITY: sw_of.setdefault(e["src"], set()).add(e["dpid"])
        n_sw = len(obj) if isinstance(obj, dict) else 0
        rows, already = tr.step(entries)
        pw.writerow([round(t0, 3), n_sw, len(entries), sum(1 for e in entries if e["prio"] >= LF.DROP_PRIORITY), "+".join(sorted(already)), round((time.time() - t0) * 1000)]); pc.flush()
        blocked = set(already)              # live view: sources that currently have a drop rule in a switch
        for src in list(hist):              # forget stale history and counters
            hist[src] = [(tt, x) for tt, x in hist[src] if t0 - tt <= STALE_S]
            if not hist[src]:
                del hist[src]; hits.pop(src, None); first_pos.pop(src, None)
        for src, r in rows.items():
            h = hist.setdefault(src, []); h.append((t0, r)); del h[:-LF.W]
            if len(h) < LF.W: continue
            v = np.array([[np.mean([x[f] for _, x in h]) for f in LF.FEATS]])[:, idx]
            if model is None:
                p = float(v[0, 0] >= rule["threshold"]) if rule["direction"] == ">=" else float(v[0, 0] <= rule["threshold"])
            else:
                p = float(model.predict_proba(v)[0, 1])
            sw.writerow([round(t0, 3), src, r["dpid"], round(p, 4)])
            fw.writerow([round(t0, 3), src, r["dpid"], round(p, 4)] + [round(float(np.mean([x[f] for _, x in h])), 3) for f in LF.FEATS])
            if p >= thr:
                hits[src] = hits.get(src, 0) + 1; first_pos.setdefault(src, t0)
            else:
                hits[src] = 0; first_pos.pop(src, None)
            if (hits[src] >= a.consecutive and src not in blocked and time.time() - recent.get(src, 0) > 5
                    and src not in NEVER_BLOCK and installs < a.max_blocks):
                if a.dry_run:
                    ok, rep = False, "dry_run"
                else:
                    targets = sorted(sw_of.get(src, {r["dpid"]})) if a.block_scope == "all" else [r["dpid"]]
                    res = [block(src, d) for d in targets]
                    ok, rep = all(x[0] for x in res), " | ".join(x[1] for x in res)
                dp_txt = "+".join(sorted(sw_of.get(src, {r["dpid"]}))) if a.block_scope == "all" else r["dpid"]
                aw.writerow([round(first_pos.get(src, t0), 3), round(time.time(), 3), src, dp_txt, ok, rep[:80], round(time.time() - last_block[src], 1) if src in last_block else "", n_sw]); ac.flush(); last_block[src] = time.time()
                print(f"[{time.strftime('%H:%M:%S')}] block {src} on {dp_txt} p={p:.2f} ok={ok}", flush=True)
                if ok: recent[src] = time.time(); installs += 1
        sc.flush(); fc.flush()
        time.sleep(max(0.0, a.interval - (time.time() - t0)))
except KeyboardInterrupt:
    pass
