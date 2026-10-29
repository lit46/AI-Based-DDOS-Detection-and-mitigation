# Reproducing the tables

Two levels. Level 1 takes minutes and needs no network setup. Level 2 re-runs the experiments.

## 0. Environment
- Python 3.x with the packages in `requirements.txt` (create it with `pip freeze > requirements.txt` inside the `tf_env` you used).
- Level 2 live loop only: Linux, Mininet, Open vSwitch, hping3, Java 11, Floodlight (`./start_floodlight.sh`), sudo.
- Data (not stored here): CIC-DDoS2019 (Sharafaldin et al., ICCST 2019), UNSW-NB15 (Moustafa and Slay, MilCIS 2015). Our SDN dataset (297,473 flows) is in `data/` or linked in the README.

## Table map (TO CONFIRM against your own folders before pushing)
| Paper / report table | What it shows | Level 1: check from saved file | Level 2: command |
|---|---|---|---|
| II / 7.2, 7.3 | selector accuracy per dataset, grouped CV, de-duplicated | `results/offline/*/summary_mean_std.csv` | the CV run script in `cv_study/` |
| III / 7.5, IV / 7.6, V / 7.7 | Hasan et al. claim and day-1 to day-2 | `results/offline/*` from `./run_hasan.sh report` | `cd cv_study && ./run_hasan.sh grouped|random|dedup|dayshift ; ./run_hasan.sh report` |
| VI / 7.8 | live TP / FN / FP per scenario | `results/live/` + `python3 live_loop/eval_loop.py --run_dir <run> --actions <actions.csv>` | `live_loop/run_variants*.sh`, then `eval_loop.py` |
| VII / 7.9 | recall by attack type (seen / unseen) | `results/` leave-one-variant-out output | the training script that wrote `train_v3.log` |
| VIII / 7.11 | selection time | `fs_sec` column of `summary_mean_std.csv`, `infer_cost_summary.csv` | same as II |
| 7.10 | random-split comparison of five models | (Colab notebook, add it under `cv_study/`) | |
| Live demo | closed loop on screen | n/a | `live_loop/demo.sh preflight` then `./demo.sh tmux syn_big` |
