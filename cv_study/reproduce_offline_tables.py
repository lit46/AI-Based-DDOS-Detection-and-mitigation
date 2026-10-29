#!/usr/bin/env python3
"""Reproduce the selector tables (paper Table II / report 7.2, 7.3, 7.11) from the saved CV results.
Pooled accuracy = mean of accuracy_mean over the three classifiers (KNN, RF, XGB) for each selector.
Selection time (Table VIII / 7.11) = mean fs_sec over classifiers.   Run:  python3 cv_study/reproduce_offline_tables.py
"""
import os, sys, pandas as pd
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results", "offline")
SETS = {"CIC-DDoS2019 (grouped CV)": "cv_cic_binary", "UNSW-NB15 (official holdout)": "final_unsw_test",
        "SDN dataset (grouped CV)": "sdn_cv", "SDN dataset (de-duplicated)": "sdn_cv_dedup"}
ANCHORS = {  # values printed in the paper text, tolerance 0.0005
 "CIC-DDoS2019 (grouped CV)": {"STD_RFE_RF": 0.9991, "SOTA_mRMR": 0.9125, "F0_Fuzzy_RAR": 0.9647, "P4_Inter_IntraWeight_Adjustment_FS": 0.9854},
 "UNSW-NB15 (official holdout)": {"STD_MI": 0.8688, "STD_RFE_RF": 0.8609, "RA_Consensus": 0.8607, "F0_Fuzzy_RAR": 0.8632, "P4_Inter_IntraWeight_Adjustment_FS": 0.8635, "WITHOUT_FS": 0.8570},
 "SDN dataset (grouped CV)": {"STD_RFE_RF": 0.9987, "SOTA_mRMR": 0.9194, "RA_Consensus": 0.9680},
}
def main():
    bad = 0; times = None
    for label, folder in SETS.items():
        f = os.path.join(ROOT, folder, "summary_mean_std.csv")
        if not os.path.exists(f): print(f"\n## {label}: MISSING {f}"); bad += 1; continue
        d = pd.read_csv(f); p = d.groupby("fs_method").agg(accuracy=("accuracy_mean", "mean"), sel_time_s=("fs_sec", "mean")).sort_values("accuracy", ascending=False)
        print(f"\n## {label}   [{folder}]"); print(p.round(4).to_string())
        for k, v in ANCHORS.get(label, {}).items():
            got = p.accuracy.get(k); ok = got is not None and abs(got - v) <= 0.0005; bad += (not ok)
            print(f"   check {k:38s} paper {v:.4f}  got {got if got is None else round(got,4)}  {'OK' if ok else 'DIFF'}")
    print("\nAll anchor values match the paper." if not bad else f"\n{bad} check(s) failed or inputs missing.")
if __name__ == "__main__": main()
