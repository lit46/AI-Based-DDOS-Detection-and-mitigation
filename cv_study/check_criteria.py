#!/usr/bin/env python3
"""check_criteria.py -- applies the PRE-REGISTERED development criteria (PROTOCOL_B.md) to the dev result folders.
  python3 check_criteria.py --unsw_dev <dir> --cic_dev <dir>
Criteria for RA_Consensus (all three must hold to be allowed one test on the official UNSW test file):
  C1 worst-case gap (max over the two dev sets, points of pooled accuracy to the best selector) <= RFE-RF's worst-case gap + 0.2
  C2 gap on each dev set <= 1.0 point
  C3 median selection time <= 3.0 s (about 2x faster than RFE-RF's ~5.5 s; relaxed from 2.0 s on 2026-10-22 BEFORE any real dev run, after a synthetic timing test)
The criteria are fixed in this file BEFORE any dev run. Do not edit them after seeing results."""
import argparse, os
import pandas as pd
ap = argparse.ArgumentParser(); ap.add_argument("--unsw_dev", required=True); ap.add_argument("--cic_dev", required=True)
ap.add_argument("--marker", default="dev_criteria_PASS"); ap.add_argument("--cand", default="RA_Consensus"); ap.add_argument("--ref", default="STD_RFE_RF")
a = ap.parse_args()
gaps, times = {}, {}
for tag, d in (("UNSW_dev", a.unsw_dev), ("CIC_dev", a.cic_dev)):
    r = pd.read_csv(os.path.join(d, "runs_per_fold.csv"))
    r = r[r.fs_method != "WITHOUT_FS"]
    acc = r.groupby("fs_method").accuracy.mean() * 100
    gaps[tag] = acc.max() - acc
    times[tag] = r[r.fs_method == a.cand].fs_sec.median()
    print(f"\n{tag}: pooled accuracy (%) by selector"); print(acc.sort_values(ascending=False).round(2).to_string())
w = lambda s: max(gaps[t][s] for t in gaps)
c1 = w(a.cand) <= w(a.ref) + 0.2
c2 = all(gaps[t][a.cand] <= 1.0 for t in gaps)
c3 = max(times.values()) <= 3.0
print(f"\nworst-case gap: {a.cand} {w(a.cand):.2f} pts, {a.ref} {w(a.ref):.2f} pts")
print(f"C1 worst-case gap <= reference + 0.2 : {'PASS' if c1 else 'FAIL'}")
print(f"C2 gap <= 1.0 pt on every dev set    : {'PASS' if c2 else 'FAIL'}  ({ {t: round(float(gaps[t][a.cand]), 2) for t in gaps} })")
print(f"C3 median selection time <= 3.0 s (about 2x faster than RFE-RF's ~5.5 s; relaxed from 2.0 s on 2026-10-22 BEFORE any real dev run, after a synthetic timing test)    : {'PASS' if c3 else 'FAIL'}  ({ {t: round(float(v), 2) for t, v in times.items()} })")
ok = c1 and c2 and c3
if ok: open(a.marker, "w").write("dev criteria passed\n")
print("\nDECISION:", "ALL PASS -> one test run on the official UNSW test file is allowed" if (c1 and c2 and c3) else "NOT ALL PASS -> stop; report as a negative result; do not tune on the test file")
