#!/usr/bin/env python3
"""Reproduce Table VI (live decisions: TP / FN / FP per scenario) from the saved runs.

For every (scenario, detector) the right run folder and actions file are taken from make_figures.py.
Each run is scored with eval_loop.py (unchanged); this script only reads its per-round table:
    TP = blocks_in_window - wrong_blocks      (attackers blocked in that round)
    FN = (number of attackers in the round) - TP
    FP = wrong_blocks                         (normal hosts wrongly blocked)
and sums them over the rounds. Run from anywhere:  python3 live_loop/reproduce_table_vi.py
"""
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
LIVE = os.path.join(HERE, "..", "results", "live")
EVAL = os.path.join(HERE, "eval_loop.py")
RUNS = [  # scenario, detector, run folder, actions file, expected (TP, FN, FP) from the paper
 ("Full-size SYN flood",   "XGBoost v3", "hm_syn_big",     "detm3_actions.csv", (4,0,0)), ("Full-size SYN flood",   "Rule", "hr_syn_big",     "detr3_actions.csv", (4,0,3)),
 ("Full-size UDP flood",   "XGBoost v3", "hm_udp_big",     "detm3_actions.csv", (4,0,0)), ("Full-size UDP flood",   "Rule", "hr_udp_big",     "detr3_actions.csv", (4,0,0)),
 ("Full-size ICMP flood",  "XGBoost v3", "im_icmp_big",    "detm4_actions.csv", (3,0,0)), ("Full-size ICMP flood",  "Rule", "ir_icmp_big",    "detr4_actions.csv", (3,0,2)),
 ("Flash crowd",           "XGBoost v3", "hm_flashcrowd",  "detm3_actions.csv", (0,0,0)), ("Flash crowd",           "Rule", "hr_flashcrowd",  "detr3_actions.csv", (0,0,5)),
 ("Heavy legitimate load", "XGBoost v3", "hvm_heavy",      "detm6_actions.csv", (0,0,6)), ("Heavy legitimate load", "Rule", "hvr_heavy",      "detr6_actions.csv", (0,0,7)), ("Heavy legitimate load", "XGBoost v4", "hv4_heavy",     "detm7_actions.csv", (0,0,0)),
 ("Heavy load plus flood", "XGBoost v3", "hvm_heavy_atk",  "detm6_actions.csv", (4,0,5)), ("Heavy load plus flood", "Rule", "hvr_heavy_atk",  "detr6_actions.csv", (4,0,9)), ("Heavy load plus flood", "XGBoost v4", "hv4_heavy_atk", "detm7_actions.csv", (3,1,0)),
]
# Round 3 of the ICMP run never carried attack traffic to the victim (target_rx_pps 81.9, about the normal level, no block possible),
# so it is excluded as one empty round, for both detectors (stated in the Table VI footnote of the paper). Key: scenario -> rounds to skip.
# Known one-count discrepancy: the published Table VI lists 9 wrong blocks for the
# rule detector in "Heavy load plus flood"; the saved logs give 10 (rounds 4+3+3),
# also confirmed by make_figures.py. All other rows match exactly.
KNOWN = {("Heavy load plus flood", "Rule"): (4, 0, 10)}
EXCLUDE_ROUNDS = {"Full-size ICMP flood": {3}}
ROW = re.compile(r"^\s*(\d+)\s+(\w+)\s+(.*)$")
def parse(text, skip=()):
    tp = fn = fp = 0
    for line in text.splitlines():
        m = ROW.match(line)
        if not m or m.group(2) in ("round",): continue
        if int(m.group(1)) in skip: continue
        toks = m.group(3).split()
        if len(toks) < 8: continue
        wrong, inwin = int(float(toks[-2])), int(float(toks[-1]))
        att = toks[0].split("+") if re.match(r"^\d+\.\d+\.\d+\.\d+(\+\d+\.\d+\.\d+\.\d+)*$", toks[0]) else []
        t = max(inwin - wrong, 0)
        tp += min(t, len(att)); fn += max(len(att) - t, 0); fp += wrong
    return tp, fn, fp
def main():
    print(f"{'Scenario':24s} {'Detector':11s} {'TP/FN/FP got':14s} {'paper':10s} match")
    bad = 0; noted = []
    for sc, det, run, act, exp in RUNS:
        rd, ap = os.path.join(LIVE, run), os.path.join(LIVE, act)
        if not (os.path.isdir(rd) and os.path.exists(ap)):
            print(f"{sc:24s} {det:11s} {'(run folder or actions file missing: ' + run + ')':s}"); bad += 1; continue
        out = subprocess.run([sys.executable, EVAL, "--run_dir", rd, "--actions", ap], capture_output=True, text=True, cwd=LIVE).stdout
        got = parse(out, EXCLUDE_ROUNDS.get(sc, ())); ok = got == exp
        known = (not ok) and KNOWN.get((sc, det)) == got
        flag = "OK" if ok else ("NOTE: logs give 10 wrong blocks" if known else "DIFF")
        print(f"{sc:24s} {det:11s} {'%d / %d / %d' % got:14s} {'%d / %d / %d' % exp:10s} {flag}")
        if known: noted.append(sc)
        elif not ok: bad += 1
    if noted: print("\nNote: 1 row differs by one wrong block (paper 9, logs 10); see comment at top of this script / REPRODUCE.md.")
    print("All other rows match Table VI exactly." if noted and not bad else ("All rows match Table VI." if not bad else f"{bad} row(s) differ or are missing."))
if __name__ == "__main__": main()
