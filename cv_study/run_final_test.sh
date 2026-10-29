#!/bin/bash
# ONE test run on the official UNSW test file. Refuses to start unless the dev criteria passed.
set -e
O=~/sdn_floodlight_dataset/output; U=~/datasets/UNSW
[ -f $O/dev_criteria_PASS ] || { echo "dev criteria not passed -> not allowed to touch the test file (PROTOCOL_B.md rule 2)"; exit 1; }
[ -d $O/final_unsw_test ] && { echo "a final test run already exists at $O/final_unsw_test (rule 5: one run only)"; exit 1; }
source ~/tf_env/bin/activate
cd ~/sdn_floodlight_dataset/cv_study
python3 -W ignore holdout_study.py --train $U/UNSW_NB15_training-set.csv --test $U/UNSW_NB15_testing-set.csv --out $O/final_unsw_test \
  --label_col label --extra_drop '^attack_cat$' --repeats 10 --models KNN,RF,XGB \
  --selectors RA_Consensus,RA_noRF,RA_mean,RA_noRed,F0_Fuzzy_RAR,P4_Inter_IntraWeight_Adjustment_FS,STD_MI,STD_ANOVA,STD_RFE_RF,SOTA_mRMR,SOTA_SHAP_XGB --jobs 4 --resume
