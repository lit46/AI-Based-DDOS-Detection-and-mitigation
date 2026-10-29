# Review 3 Live Demo Run-Sheet (about 6 minutes on stage)

Project: Adaptive AI-Based DDoS Detection and Mitigation in SDN. Run everything from the project folder.

## Before you leave (tonight)
1. `chmod +x demo.sh && ./demo.sh preflight`  -> must print PREFLIGHT PASSED.
2. Do one full dry run: `./demo.sh tmux syn_big`, wait for a block line, then `./demo.sh eval`.
3. Charge the laptop, keep the charger. Close browsers and heavy apps (the live-load tests are sensitive).
4. Keep a recorded screen capture of the dry run as a backup.

## 15 minutes before your slot
- `./demo.sh clean` then `./demo.sh preflight`.
- Font size large in all terminals. Connect projector first, then start the demo.

## The demo (maps to Report Chapter 6)
| Step | Terminal | Command | What to say / what you should see |
|---|---|---|---|
| 1 | T1 | `./demo.sh controller` | Floodlight on 127.0.0.1:8080. Wait about 20 s. |
| 2 | T3 | `./demo.sh detector syn_big` | XGBoost v3 detector polling roughly every 1 s, 11 per-source features averaged over 3 polls. |
| 3 | T2 | `./demo.sh topo syn_big` | 3 switches, normal hosts h1-h3, h6, attackers h4 and h5. Each round: 30 s normal, 20 s attack, 15 s cool-down. |
| 4 | T3 | watch | `block 10.0.0.4 on <switch> p=0.99 ok=True` a few seconds after the flood starts (measured 4 to 17 s). Rule fires after 2 consecutive scores of 0.5 or more. |
| 5 | any | `./demo.sh rules` | Priority-40000 drop entries for the attacker address. |
| 6 | any | `./demo.sh eval` | Expected for syn_big (v3): 4 of 4 attacker decisions blocked, 0 wrong blocks. |

If time allows (second run, same terminals, restart T3 with the new variant):
- **Flash crowd**: `./demo.sh detector flashcrowd` + `./demo.sh topo flashcrowd` -> no block (rule baseline would block 5 normal hosts).
- **Heavy legitimate load**: run with `heavy` -> the script picks v4 (v3 made 6 wrong blocks, v4 made 0).
- **Rule baseline**: `./demo.sh rule` then the same topo -> wrong blocks on normal hosts in SYN and flash-crowd.

## Numbers to have ready (Table VI in the paper)
- Original lab series: blocked 32 of 33 attack rounds, 0 blocks in 9 flash-crowd rounds, time to block 4 to 17 s.
- Full-size SYN 4/0/0, UDP 4/0/0, ICMP 3/0/0 (TP/FN/FP) for v3. Rule baseline wrong blocks: SYN 3, UDP 0, ICMP 2.
- Heavy load plus flood: v4 blocked 3 of 4 attackers with 0 wrong blocks (one miss).
- Limits to admit honestly: low-rate SYN not detected, unseen ICMP only partly detected, one Floodlight ClassCastException under a full-size UDP flood (switches reconnected, rules cleared, re-blocked about 4.6 s later, cause not found).

## If something breaks
| Problem | Fix |
|---|---|
| Port 8080 busy / old Floodlight | `./demo.sh clean`, restart T1 |
| Mininet complains about leftovers | `sudo mn -c` |
| No block line appears | Check T1 is up (`curl localhost:8080/wm/core/controller/switches/json`), restart detector, rerun topo |
| ClassCastException on a UDP run | This is the known failure in the report (report Section 7.5). Say so, rerun once, then move on |
| Anything dead after 2 tries | Play the recorded dry-run video, then show Table VI |

## Safety line for the examiners
All attack traffic is hping3 from Mininet hosts to h1 only; attacker addresses are dropped at the NAT node; the detector never blocks the NAT address; nothing was run against any public or institutional network.
