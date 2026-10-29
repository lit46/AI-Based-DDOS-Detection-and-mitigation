#!/usr/bin/env python3
"""eval_loop.py -- summarise a closed-loop test: time to block, false blocks, and attack packets reaching the target before/after the block."""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
ap = argparse.ArgumentParser()
ap.add_argument("--run_dir", required=True); ap.add_argument("--actions", required=True); ap.add_argument("--out", default="loop_eval.csv")
a = ap.parse_args()
ev = pd.read_csv(f"{a.run_dir}/events.csv"); tr = pd.read_csv(f"{a.run_dir}/traffic.csv")
ac = pd.read_csv(a.actions); ac = ac[ac.ok == True] if len(ac) else ac
tr["rx"] = pd.to_numeric(tr.rx_packets, errors="coerce"); tr["pps"] = tr.rx.diff().clip(lower=0)
rows = []
for i, e in ev.iterrows():
    atk = set(filter(None, str(e.attackers).split("+"))) if e.attackers == e.attackers else set()
    inw = ac[(ac.t_block >= e.t_start) & (ac.t_block <= e.t_end + 10)] if len(ac) else ac
    good = inw[inw.src.isin(atk)] if len(inw) else inw
    first = good.t_block.min() if len(good) else np.nan
    allb = len(inw)
    last = good.t_block.max() if len(good) and set(good.src) >= atk else np.nan
    before = tr[(tr.t >= e.t_start) & (tr.t <= (first if first == first else e.t_end))].pps.mean()
    after = tr[(tr.t >= first + 3) & (tr.t <= e.t_end)].pps.mean() if first == first else np.nan
    after_all = tr[(tr.t >= last + 3) & (tr.t <= e.t_end)].pps.mean() if last == last else np.nan
    rows.append(dict(round=i + 1, kind=e.kind, attackers=e.attackers if e.attackers == e.attackers else '', pps_sent=e.pps, time_to_first_block_s=first - e.t_start, time_to_all_blocked_s=last - e.t_start,
                     target_rx_pps_before_block=before, target_rx_pps_after_first_block=after, target_rx_pps_after_all_blocked=after_all,
                     wrong_blocks=int((~inw.src.isin(atk)).sum()) if len(inw) else 0, blocks_in_window=allb))
r = pd.DataFrame(rows); r.to_csv(a.out, index=False); print(r.round(2).to_string(index=False))
if len(ac):
    import loop_features as LF
    inany = np.zeros(len(ac), bool)
    for _, e in ev.iterrows(): inany |= ((ac.t_block >= e.t_start) & (ac.t_block <= e.t_end + 10)).values
    print("\nblocks on NORMAL hosts over the whole run (any time):", int((~ac.src.isin(LF.ATTACKERS)).sum()),
          "| attacker blocks outside every attack window:", int((ac.src.isin(LF.ATTACKERS).values & ~inany).sum()), "| total blocks:", len(ac))
print("rounds with an attacker blocked: %d / %d" % (r.time_to_first_block_s.notna().sum(), int((r.kind == 'attack').sum())))
