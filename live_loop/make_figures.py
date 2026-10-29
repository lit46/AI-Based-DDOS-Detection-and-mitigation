#!/usr/bin/env python3
"""make_figures.py -- turns the live-run folders into figures for presentation. Run in the sdn_loop folder:  python3 make_figures.py
Reads, per run: <run_dir>/traffic.csv (t, cumulative rx packets at the victim), <run_dir>/events.csv, and the detector's *_actions.csv.
Writes PNG files into ./figures/. Runs whose folders are missing are skipped. Nothing here changes any data."""
import os, sys
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ATTACKERS = {"10.0.0.4", "10.0.0.5"}
# (variant label, detector label, run folder, detector actions file)
RUNS = [
    ("syn_big",    "XGBoost v3", "hm_syn_big",    "detm3_actions.csv"), ("syn_big",    "Rule", "hr_syn_big",    "detr3_actions.csv"),
    ("udp_big",    "XGBoost v3", "hm_udp_big",    "detm3_actions.csv"), ("udp_big",    "Rule", "hr_udp_big",    "detr3_actions.csv"),
    ("icmp_big",   "XGBoost v3", "im_icmp_big",   "detm4_actions.csv"), ("icmp_big",   "Rule", "ir_icmp_big",   "detr4_actions.csv"),
    ("flash crowd","XGBoost v3", "hm_flashcrowd", "detm3_actions.csv"), ("flash crowd","Rule", "hr_flashcrowd", "detr3_actions.csv"),
    ("heavy",      "XGBoost v3", "hvm_heavy",     "detm6_actions.csv"), ("heavy",      "Rule", "hvr_heavy",     "detr6_actions.csv"), ("heavy", "XGBoost v4", "hv4_heavy", "detm7_actions.csv"),
    ("heavy+flood","XGBoost v3", "hvm_heavy_atk", "detm6_actions.csv"), ("heavy+flood","Rule", "hvr_heavy_atk", "detr6_actions.csv"), ("heavy+flood", "XGBoost v4", "hv4_heavy_atk", "detm7_actions.csv"),
]
COL = {"XGBoost v3": "#2a6fb0", "Rule": "#c0522d", "XGBoost v4": "#2e8b57"}

def load(run, actions):
    if not (os.path.isdir(run) and os.path.exists(os.path.join(run, "traffic.csv")) and os.path.exists(actions)):
        return None
    tr = pd.read_csv(os.path.join(run, "traffic.csv")); tr["rx_packets"] = pd.to_numeric(tr.rx_packets, errors="coerce")
    tr = tr.dropna().reset_index(drop=True); tr["pps"] = tr.rx_packets.diff() / tr.t.diff(); tr = tr.dropna()
    ev = pd.read_csv(os.path.join(run, "events.csv")); ac = pd.read_csv(actions)
    ac = ac[(ac.t_block >= tr.t.min()) & (ac.t_block <= tr.t.max() + 5)]          # only blocks that happened during this run
    return tr, ev, ac

def timeline(items, path, title):
    fig, axes = plt.subplots(len(items), 1, figsize=(10, 2.3 * len(items)), sharex=False, squeeze=False)
    for ax, (lab, det, tr, ev, ac) in zip(axes[:, 0], items):
        t0 = tr.t.min(); ax.plot(tr.t - t0, tr.pps.clip(lower=0), color=COL.get(det, "k"), lw=1.2)
        for _, e in ev.iterrows():
            colr = "#d9534f" if e.kind == "attack" else "#6aa84f"
            ax.axvspan(e.t_start - t0, e.t_end - t0, color=colr, alpha=0.15, lw=0)
        for _, b in ac.iterrows():
            bad = b.src not in ATTACKERS
            ax.axvline(b.t_block - t0, color="#b00020" if bad else "#222222", ls="--" if not bad else "-", lw=1.1)
            ax.text(b.t_block - t0, ax.get_ylim()[1] * 0.92, b.src.replace("10.0.0.", "h"), fontsize=7, rotation=90, va="top", ha="right")
        ax.set_ylabel("packets/s to h1"); ax.set_title(f"{lab} - {det}", fontsize=10, loc="left"); ax.grid(alpha=0.25)
    axes[-1, 0].set_xlabel("seconds since run start")
    fig.suptitle(title + "\nred band = attack, green band = legitimate heavy load; dashed line = attacker blocked, solid red = NORMAL host blocked", fontsize=9)
    fig.tight_layout(rect=(0, 0, 1, 0.94)); fig.savefig(path, dpi=150); plt.close(fig)

def main():
    os.makedirs("figures", exist_ok=True); got, rows = [], []
    for var, det, run, act in RUNS:
        r = load(run, act)
        if r is None: print("skip (missing):", run, act); continue
        tr, ev, ac = r; wrong = int((~ac.src.isin(ATTACKERS)).sum()); good = int(ac.src.isin(ATTACKERS).sum())
        rows.append(dict(variant=var, detector=det, run=run, attacker_blocks=good, normal_host_blocks=wrong)); got.append((var, det, tr, ev, ac))
    if not rows: sys.exit("no run folders found - run this inside the sdn_loop folder")
    df = pd.DataFrame(rows); df.to_csv("figures/summary_blocks.csv", index=False); print(df.to_string(index=False))
    # figure 1: wrong blocks per variant and detector
    vars_ = list(dict.fromkeys(df.variant)); dets = list(dict.fromkeys(df.detector)); w = 0.8 / len(dets)
    fig, ax = plt.subplots(figsize=(9, 4))
    for i, d in enumerate(dets):
        v = [int(df[(df.variant == x) & (df.detector == d)].normal_host_blocks.sum()) for x in vars_]
        ax.bar(np.arange(len(vars_)) + i * w, v, w, label=d, color=COL.get(d))
        for xx, vv in zip(np.arange(len(vars_)) + i * w, v): ax.text(xx, vv + 0.1, str(vv), ha="center", fontsize=8)
    ax.set_xticks(np.arange(len(vars_)) + 0.4 - w / 2); ax.set_xticklabels(vars_); ax.set_ylabel("blocks on normal hosts"); ax.legend()
    ax.set_title("Wrong blocks (normal hosts blocked) per test, 3 rounds each"); ax.grid(axis="y", alpha=0.25)
    fig.tight_layout(); fig.savefig("figures/fig1_wrong_blocks.png", dpi=150); plt.close(fig)
    # figure 2..: timelines grouped by variant
    for v in vars_:
        items = [(f"{v}", d, tr, ev, ac) for (vv, d, tr, ev, ac) in got if vv == v]
        timeline(items, f"figures/fig_timeline_{v.replace(' ', '_').replace('+', '_')}.png", f"Packets per second reaching the victim h1 - {v}")
    print("wrote figures/ :", sorted(os.listdir("figures")))
main()
