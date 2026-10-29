"""loop_features.py -- shared by collector, trainer and detector so training and deployment see identical features.
Features are computed per source IP from Floodlight flow-entry counters (OpenFlow flow stats), one row per poll, then averaged
over the last W polls. Lab use only."""
import json
import numpy as np

ATTACKERS = ("10.0.0.4", "10.0.0.5")      # ground truth for LABELLING only; the detector never uses it
DROP_PRIORITY = 40000                      # priority of the drop rules the detector installs (ignored when computing features)
W = 3                                      # rolling window (polls)
FEATS = ["n_entries", "new_entries", "d_packets", "d_bytes", "mean_pkt_size", "mean_pkts_per_entry", "frac_small_entries",
         "max_entry_packets", "mean_duration_s", "n_dst_ips", "n_dst_ports"]


def parse_flows(obj):
    """Floodlight /wm/core/switch/all/flow/json (or a single-switch reply) -> list of entry dicts that match on an IPv4 source."""
    if obj is None:
        return []
    items = obj.items() if "flows" not in obj else [("unknown", obj)]
    out = []
    for dpid, rep in items:
        if not isinstance(rep, dict):
            continue
        for fl in rep.get("flows", []) or []:
            m = fl.get("match", {}) or {}
            src = m.get("ipv4_src") or m.get("nw_src")
            if not src:
                continue
            out.append(dict(
                dpid=str(dpid), src=str(src).split("/")[0],
                dst=str(m.get("ipv4_dst") or m.get("nw_dst") or "").split("/")[0],
                dport=str(m.get("tcp_dst") or m.get("udp_dst") or m.get("tp_dst") or ""),
                packets=int(fl.get("packet_count", 0)), nbytes=int(fl.get("byte_count", 0)),
                dur=float(fl.get("duration_sec", 0)) + float(fl.get("duration_nsec", 0)) / 1e9,
                prio=int(fl.get("priority", 0)),
                key=(str(dpid), json.dumps(m, sort_keys=True), int(fl.get("priority", 0)), int(fl.get("cookie", 0)))))
    return out


class Tracker:
    """Turns successive flow-stat snapshots into one feature row per source IP (taken at the switch that sees most of its packets)."""

    def __init__(self):
        self.prev = {}

    def step(self, entries):
        cur, grp, blocked = {}, {}, set()
        for e in entries:
            if e["prio"] >= DROP_PRIORITY:
                blocked.add(e["src"]); continue
            cur[e["key"]] = (e["packets"], e["nbytes"])
            p0, b0 = self.prev.get(e["key"], (0, 0))
            e["dp"] = e["packets"] - p0 if e["packets"] >= p0 else e["packets"]
            e["db"] = e["nbytes"] - b0 if e["nbytes"] >= b0 else e["nbytes"]
            e["new"] = e["key"] not in self.prev
            grp.setdefault((e["src"], e["dpid"]), []).append(e)
        self.prev = cur
        best = {}
        for (src, dpid), es in grp.items():
            pk = np.array([x["packets"] for x in es], float)
            row = dict(dpid=dpid, n_entries=len(es), new_entries=sum(x["new"] for x in es),
                       d_packets=float(sum(x["dp"] for x in es)), d_bytes=float(sum(x["db"] for x in es)),
                       mean_pkt_size=float(sum(x["db"] for x in es)) / max(1.0, float(sum(x["dp"] for x in es))),
                       mean_pkts_per_entry=float(pk.mean()), frac_small_entries=float((pk <= 2).mean()),
                       max_entry_packets=float(pk.max()), mean_duration_s=float(np.mean([x["dur"] for x in es])),
                       n_dst_ips=len({x["dst"] for x in es}), n_dst_ports=len({x["dport"] for x in es if x["dport"]}))
            if src not in best or row["d_packets"] > best[src]["d_packets"]:
                best[src] = row
        return best, blocked


def window_vector(rows, feats=FEATS):
    """Mean of each feature over the last W raw rows (list of dicts)."""
    return [float(np.mean([r[f] for r in rows])) for f in feats]
