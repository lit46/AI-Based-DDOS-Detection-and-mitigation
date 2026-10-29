#!/bin/bash
# Test of the Hasan et al. (2025) "top-5 features lose < 1 point" claim. Pre-registered in PROTOCOL_C.md.
# usage:  ./run_hasan.sh prep | smoke | grouped | dedup | random | day | report
set -e
source ~/tf_env/bin/activate
cd ~/sdn_floodlight_dataset/cv_study
CSV=${CSV:-$HOME/cic_prepared_patched.csv}
O=~/sdn_floodlight_dataset/output; H=$O/hasan_data
SEL=HASAN_Top5_Published,HASAN_XGB_Gain5,STD_RFE_RF,STD_MI,SOTA_SHAP_XGB,STD_ANOVA,SOTA_mRMR
COMMON="--label_col attack_type --k 5 --drop_ports --models RF,XGB --selectors $SEL --jobs 4 --resume --no_stats --no_plots"
case "$1" in
  prep)    python3 hasan_prepare.py --csv "$CSV" --out_dir $H && python3 hasan_precheck.py --csv $H/hasan5.csv --label_col attack_type ;;
  smoke)   T0=$SECONDS; python3 -W ignore cv_study.py --csv $H/hasan5.csv --out $O/hasan_smoke --mode main --repeats 1 --folds 10 --max_folds 1 $COMMON 2>&1 | tail -3; echo "ONE UNIT TOOK $((SECONDS-T0)) s (includes loading); a full protocol run is about 30 x that / 4"  ;;
  grouped) python3 -W ignore cv_study.py --csv $H/hasan5.csv --out $O/hasan_grouped --mode main --repeats 3 --folds 10 $COMMON ;;
  dedup)   python3 -W ignore cv_study.py --csv $H/hasan5.csv --out $O/hasan_dedup --mode main --repeats 3 --folds 10 --dedup $COMMON ;;
  random)  python3 -W ignore cv_study.py --csv $H/hasan5.csv --out $O/hasan_random --mode main --repeats 3 --folds 10 --no_group_dups $COMMON ;;
  day)     [ -f $H/hasan5_day1.csv ] || { echo "no day files (the prepared CSV has no train_day/test_day in __day)"; exit 1; }
           python3 -W ignore holdout_study.py --train $H/hasan5_day1.csv --test $H/hasan5_day2.csv --out $O/hasan_day --repeats 5 $COMMON ;;
  report)  R=""; for t in grouped dedup random day; do [ -f $O/hasan_$t/runs_per_fold.csv ] && R="$R $t=$O/hasan_$t"; done
           python3 hasan_claim_report.py --runs $R --out $O/hasan_report ;;
  *) echo "usage: $0 prep|smoke|grouped|dedup|random|day|report"; exit 1 ;;
esac
