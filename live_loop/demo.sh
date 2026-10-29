#!/usr/bin/env bash
# Review 3 live demo launcher - Adaptive AI-Based DDoS Detection and Mitigation in SDN
# Run from the project directory (the one containing detector.py, topo_loop.py, eval_loop.py, loop_model_v3/, loop_model_v4/).
# Usage:  ./demo.sh <command> [variant]
#   preflight          check files, ports, leftovers (run this 30 min before)
#   tmux [variant]     open 3 panes (T1 controller, T2 topology, T3 detector) in one tmux window
#   controller         T1: start Floodlight
#   detector [variant] T3: start the XGBoost detector (model picked from the variant)
#   rule               T3: start the one-feature rule baseline instead
#   topo [variant]     T2: start Mininet + attack scenario (needs sudo)
#   rules              show priority-40000 drop rules installed in the switches
#   eval               score the last run
#   clean              stop leftovers (mn -c, stray java/python)
# Variants: syn_big (default) udp_big icmp_big flashcrowd heavy heavy_atk
set -u
DIR="${DEMO_DIR:-$PWD}"
# Java location: use $JAVA_HOME if set, else Java 11, then 8, then 17 under /usr/lib/jvm
# (on Arch: java-11-openjdk; some installs use jre11-openjdk or a versioned name).
detect_java() {
  if [ -n "${JAVA_HOME:-}" ] && [ -x "$JAVA_HOME/bin/java" ]; then echo "$JAVA_HOME"; return; fi
  for d in /usr/lib/jvm/java-11-openjdk /usr/lib/jvm/java-11* /usr/lib/jvm/*11* /usr/lib/jvm/java-8-openjdk /usr/lib/jvm/java-17-openjdk; do
    [ -x "$d/bin/java" ] && { echo "$d"; return; }
  done
  echo ""
}
JAVA_HOME_DEFAULT="$(detect_java)"
VARIANT="${2:-syn_big}"
RUN_DIR="demo_run"

# v3 was trained without the heavy-load variants; v4 adds them (Chapter 7.5).
model_for() {
  case "$1" in
    heavy|heavy_atk) echo loop_model_v4 ;;
    *)               echo loop_model_v3 ;;
  esac
}

cmd="${1:-help}"
cd "$DIR" || exit 1

case "$cmd" in
  preflight)
    ok=1
    for f in start_floodlight.sh detector.py topo_loop.py eval_loop.py rule_best.json; do
      [ -e "$f" ] && echo "ok   $f" || { echo "MISSING $f"; ok=0; }
    done
    for d in loop_model_v3 loop_model_v4; do
      [ -d "$d" ] && echo "ok   $d/" || { echo "MISSING $d/"; ok=0; }
    done
    command -v hping3 >/dev/null && echo "ok   hping3" || { echo "MISSING hping3"; ok=0; }
    command -v mn >/dev/null && echo "ok   mininet" || { echo "MISSING mininet"; ok=0; }
    if [ -n "$JAVA_HOME_DEFAULT" ]; then echo "ok   java11 ($JAVA_HOME_DEFAULT)"
    else echo "MISSING Java 11 under /usr/lib/jvm (found: $(ls /usr/lib/jvm 2>/dev/null | tr '\n' ' '))  -> export JAVA_HOME=<path> and rerun"; ok=0; fi
    if ss -ltn 2>/dev/null | grep -q ':8080 '; then echo "WARN port 8080 already in use (old Floodlight?)  -> ./demo.sh clean"; ok=0; fi
    [ "$ok" = 1 ] && echo "PREFLIGHT PASSED" || echo "PREFLIGHT HAS PROBLEMS"
    ;;
  controller)
    echo "[T1] Floodlight on 127.0.0.1:8080"
    JAVA_HOME="${JAVA_HOME:-$JAVA_HOME_DEFAULT}" ./start_floodlight.sh
    ;;
  detector)
    M=$(model_for "$VARIANT")
    echo "[T3] detector with $M (variant $VARIANT)"
    python3 -W ignore detector.py --model_dir "$M" --log demo
    ;;
  rule)
    echo "[T3] one-feature rule baseline"
    python3 -W ignore detector.py --rule rule_best.json
    ;;
  topo)
    echo "[T2] topology + scenario $VARIANT (3 rounds: 30 s normal, 20 s attack, 15 s cool-down each, about 3.5 min)"
    sudo python3 topo_loop.py --scenario loop --rounds 3 --variant "$VARIANT" --out_dir "$RUN_DIR"
    ;;
  rules)
    curl -s localhost:8080/wm/core/switch/all/flow/json | python3 -c '
import sys, json
d = json.load(sys.stdin)
n = 0
for sw, v in d.items():
    for f in v.get("flows", []):
        if str(f.get("priority")) == "40000":
            n += 1
            print(sw, "priority 40000", json.dumps(f.get("match", {})))
print(n, "drop rule(s) found")'
    ;;
  eval)
    python3 eval_loop.py --run_dir "$RUN_DIR" --actions demo_actions.csv
    ;;
  clean)
    sudo mn -c >/dev/null 2>&1
    pkill -f detector.py 2>/dev/null
    pkill -f floodlight 2>/dev/null
    pkill hping3 2>/dev/null
    echo "cleaned"
    ;;
  tmux)
    command -v tmux >/dev/null || { echo "tmux not installed - open three terminals and run controller / topo / detector"; exit 1; }
    S=demo
    tmux kill-session -t $S 2>/dev/null
    tmux new-session -d -s $S -c "$DIR" "$0 controller"
    tmux split-window -h -t $S -c "$DIR" "sleep 20; $0 detector $VARIANT; bash"
    tmux split-window -v -t $S -c "$DIR" "echo 'T2 ready. Wait for the controller (about 20 s), then press Enter to start the topology.'; read; $0 topo $VARIANT; bash"
    tmux attach -t $S
    ;;
  *)
    sed -n '2,15p' "$0"
    ;;
esac
