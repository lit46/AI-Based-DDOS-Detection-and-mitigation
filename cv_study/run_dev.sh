#!/bin/bash
# Development run for RA_Consensus (PROTOCOL_B.md). Does NOT read the official UNSW test file.
set -e
source ~/tf_env/bin/activate
cd ~/sdn_floodlight_dataset/cv_study
U=~/datasets/UNSW; O=~/sdn_floodlight_dataset/output
SEL=RA_Consensus,RA_noRF,RA_mean,RA_noRed,F0_Fuzzy_RAR,P4_Inter_IntraWeight_Adjustment_FS,STD_MI,STD_ANOVA,STD_RFE_RF,SOTA_mRMR,SOTA_SHAP_XGB
echo "[1/4] dev split  $(date)"
python3 make_dev_split.py $U/UNSW_NB15_training-set.csv $U/dev
echo "[2/4] UNSW dev  $(date)"
python3 -W ignore holdout_study.py --train $U/dev/dev_train.csv --test $U/dev/dev_val.csv --out $O/dev_unsw \
  --label_col label --extra_drop '^attack_cat$' --repeats 5 --models KNN,RF,XGB --selectors $SEL --jobs 4 --resume
echo "[3/4] CIC dev  $(date)"
python3 -W ignore cv_study.py --csv ~/cic_prepared_patched.csv --out $O/dev_cic --label_col label --drop_ports \
  --mode main --repeats 1 --folds 10 --models KNN,RF,XGB --selectors $SEL --jobs 4 --resume --no_stats
echo "[4/4] criteria  $(date)"
python3 check_criteria.py --unsw_dev $O/dev_unsw --cic_dev $O/dev_cic --marker $O/dev_criteria_PASS
echo "DEV DONE  $(date)"
