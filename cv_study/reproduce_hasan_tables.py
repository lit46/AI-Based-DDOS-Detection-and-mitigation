#!/usr/bin/env python3
"""Reproduce the Hasan et al. tables (paper Tables IV and V / report 7.6, 7.7) from saved results.
Reads results/offline/hasan_{grouped,random,dedup,day,day_xgbh}/summary_mean_std.csv.
loss (percentage points) = accuracy(all features) - accuracy(selected 5 features), per model.
Run from the repo root:  python3 cv_study/reproduce_hasan_tables.py
"""
import os, sys, pandas as pd
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "offline")
PROTO = {"Duplicate-grouped CV": "hasan_grouped", "Random split": "hasan_random",
         "De-duplicated, grouped CV": "hasan_dedup", "Day 1 to day 2": "hasan_day"}
EXTRA_DAY = "hasan_day_xgbh"
# Table IV values in the paper: protocol -> (RF all, RF top5, RF loss, XGB all, XGB top5, XGB loss)
T4 = {"Duplicate-grouped CV": (0.9896, 0.9885, 0.11, 0.9877, 0.9829, 0.48),
      "Random split": (0.9899, 0.9886, 0.13, 0.9887, 0.9839, 0.48),
      "De-duplicated, grouped CV": (0.9923, 0.9894, 0.29, 0.9906, 0.9817, 0.88),
      "Day 1 to day 2": (None, 0.9849, None, 0.9877, 0.9842, 0.34)}
# Table V losses (pp): selector -> (grouped, random, dedup, day XGB)
T5 = {"HASAN_Top5_Published": (0.11, 0.13, 0.29, 0.34), "HASAN_XGB_Gain5": (2.74, 10.8, 0.27, 15.3),
      "SOTA_SHAP_XGB": (0.78, 0.73, 1.13, 16.7), "SOTA_mRMR": (12.6, 4.55, 1.03, 29.5),
      "STD_ANOVA": (7.85, 5.38, 2.16, 29.4), "STD_MI": (7.82, 5.35, 2.16, 29.5), "STD_RFE_RF": (6.66, 3.43, 2.00, 27.0)}
TOL_ACC, TOL_LOSS = 0.0006, 0.06
def load(folder):
    f = os.path.join(ROOT, folder, "summary_mean_std.csv")
    return pd.read_csv(f) if os.path.exists(f) else None
def all_name(methods):
    for m in methods:
        u = m.upper()
        if "WITHOUT" in u or u in ("ALL", "ALL_FEATURES", "HASAN_ALL", "F_ALL", "NONE", "NO_FS"): return m
    return None
def acc(d, model, method):
    r = d[(d.model == model) & (d.fs_method == method)]
    return float(r.accuracy_mean.iloc[0]) if len(r) else None
def chk(label, got, want, tol, bad):
    if want is None or got is None: return bad, "n/a"
    ok = abs(got - want) <= tol; return bad + (not ok), ("OK" if ok else f"DIFF (paper {want})")
def main():
    bad = 0; miss = 0; data = {}
    for p, folder in PROTO.items():
        d = load(folder)
        if d is None: print(f"MISSING results/offline/{folder}"); miss += 1; continue
        data[p] = d
        print(f"\n## {p}  [{folder}]   models: {sorted(d.model.unique())}")
        print(d.pivot_table(index="fs_method", columns="model", values="accuracy_mean").round(4).to_string())
    print("\n==== Table IV: all features vs Hasan published top-5 ====")
    print(f"{'Protocol':28s} {'model':4s} {'all':>8s} {'top5':>8s} {'loss(pp)':>9s}  check")
    for p, d in data.items():
        an = all_name(d.fs_method.unique())
        for i, model in enumerate(("RF", "XGB")):
            a = acc(d, model, an) if an else None; t = acc(d, model, "HASAN_Top5_Published")
            loss = None if a is None or t is None else (a - t) * 100
            w = T4[p][3 * i: 3 * i + 3]
            res = []
            for g, v, tol in ((a, w[0], TOL_ACC), (t, w[1], TOL_ACC), (loss, w[2], TOL_LOSS)):
                bad, s = chk(p, g, v, tol, bad); res.append(s)
            f = lambda x, n: "-" if x is None else f"{x:.{n}f}"
            print(f"{p:28s} {model:4s} {f(a,4):>8s} {f(t,4):>8s} {f(loss,2):>9s}  {res}")
    if not data or all_name(next(iter(data.values())).fs_method.unique()) is None:
        print("\n(!) could not find an all-features row; check fs_method names in the printed pivots above.")
    print("\n==== Table V: accuracy loss (pp) of 5-feature selectors (RF for grouped/random/dedup, XGB for day) ====")
    print(f"{'Selector':24s} {'grouped':>8s} {'random':>8s} {'dedup':>8s} {'day':>8s}  check")
    order = ["Duplicate-grouped CV", "Random split", "De-duplicated, grouped CV", "Day 1 to day 2"]
    for sel, want in T5.items():
        row = []; res = []
        for p, w in zip(order, want):
            d = data.get(p)
            loss = None
            if d is not None and all_name(d.fs_method.unique()):
                m = "XGB" if p == "Day 1 to day 2" else "RF"
                a, s = acc(d, m, all_name(d.fs_method.unique())), acc(d, m, sel)
                if a is not None and s is not None: loss = (a - s) * 100
            row.append("-" if loss is None else f"{loss:.2f}")
            bad, r = chk(sel, loss, w, TOL_LOSS * 5 if w > 5 else TOL_LOSS, bad); res.append(r)
        print(f"{sel:24s} {row[0]:>8s} {row[1]:>8s} {row[2]:>8s} {row[3]:>8s}  {res}")
    print("Day 1 to day 2, RF 'all features' (0.7358, marked dagger in the paper) is a known failure mode of that run, not a typo.")
    print("\nAll checked values match the paper." if not bad and not miss else f"\n{bad} value(s) differ, {miss} input folder(s) missing.")
if __name__ == "__main__": main()
