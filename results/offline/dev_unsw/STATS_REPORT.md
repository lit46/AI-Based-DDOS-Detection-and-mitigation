# Statistical validation (metric: accuracy)

Interpretation notes
- 'Win/Tie/Loss' (your 'wintaylor's') is implemented as Win/Tie/Loss: Win = proposed accuracy higher by more than the tolerance (0.001), Tie = within tolerance, Loss = lower.
- Folds of one CV share training data and repeats reuse the same rows, so blocks are positively correlated; p-values are anti-conservative (Nadeau & Bengio 2003). Use them to rank methods, not as exact error rates.
- With n paired blocks the smallest two-sided Wilcoxon p is 2/2^n; n=5 repeats cannot go below 0.0625, so fold-level blocks (n = repeats x folds) are used.
- Holm correction is applied per (scope, reference method).

## Friedman + Iman-Davenport

| scope                    |   N |   k |     chi2 |   p_friedman |   F_iman_davenport |   df1 |   df2 |   p_iman_davenport |
|:-------------------------|----:|----:|---------:|-------------:|-------------------:|------:|------:|-------------------:|
| KNN__fold_level          |   5 |  12 |  40.9902 |        2e-05 |           11.7033  |    11 |    44 |                  0 |
| RF__fold_level           |   5 |  12 |  41.9601 |        2e-05 |           12.8713  |    11 |    44 |                  0 |
| XGB__fold_level          |   5 |  12 |  38.9888 |        5e-05 |            9.74038 |    11 |    44 |                  0 |
| ALL_MODELS__fold_level   |  15 |  12 | 102.633  |        0     |           23.039   |    11 |   154 |                  0 |
| ALL_MODELS__repeat_level |  15 |  12 | 102.633  |        0     |           23.039   |    11 |   154 |                  0 |

## Nemenyi critical difference

| scope                    |   k |   N |   alpha |   q_alpha_over_sqrt2 |   critical_difference |
|:-------------------------|----:|----:|--------:|---------------------:|----------------------:|
| KNN__fold_level          |  12 |   5 |    0.05 |                3.268 |                7.4522 |
| RF__fold_level           |  12 |   5 |    0.05 |                3.268 |                7.4522 |
| XGB__fold_level          |  12 |   5 |    0.05 |                3.268 |                7.4522 |
| ALL_MODELS__fold_level   |  12 |  15 |    0.05 |                3.268 |                4.3025 |
| ALL_MODELS__repeat_level |  12 |  15 |    0.05 |                3.268 |                4.3025 |

### Average ranks: ALL_MODELS__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |     1.5333 |        0.9347 |       0.0112 | no_fs     |
| P4_Inter_IntraWeight_Adjustment_FS |     4.1    |        0.9321 |       0.0067 | proposed  |
| F0_Fuzzy_RAR                       |     4.4333 |        0.9294 |       0.0103 | proposed  |
| RA_mean                            |     4.9    |        0.9296 |       0.0109 | proposed  |
| SOTA_SHAP_XGB                      |     5.5667 |        0.9286 |       0.0131 | benchmark |
| STD_MI                             |     5.9    |        0.9298 |       0.008  | classic   |
| SOTA_mRMR                          |     6.0667 |        0.929  |       0.01   | benchmark |
| STD_RFE_RF                         |     7.3    |        0.9265 |       0.0133 | classic   |
| RA_Consensus                       |     7.5333 |        0.9271 |       0.0112 | proposed  |
| RA_noRF                            |     8.2    |        0.9265 |       0.0113 | proposed  |
| RA_noRed                           |    10.6    |        0.9228 |       0.0122 | proposed  |
| STD_ANOVA                          |    11.8667 |        0.907  |       0.0346 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=4.303): WITHOUT_FS, P4_Inter_IntraWeight_Adjustment_FS, F0_Fuzzy_RAR, RA_mean, SOTA_SHAP_XGB

### Average ranks: ALL_MODELS__repeat_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |     1.5333 |        0.9347 |       0.0112 | no_fs     |
| P4_Inter_IntraWeight_Adjustment_FS |     4.1    |        0.9321 |       0.0067 | proposed  |
| F0_Fuzzy_RAR                       |     4.4333 |        0.9294 |       0.0103 | proposed  |
| RA_mean                            |     4.9    |        0.9296 |       0.0109 | proposed  |
| SOTA_SHAP_XGB                      |     5.5667 |        0.9286 |       0.0131 | benchmark |
| STD_MI                             |     5.9    |        0.9298 |       0.008  | classic   |
| SOTA_mRMR                          |     6.0667 |        0.929  |       0.01   | benchmark |
| STD_RFE_RF                         |     7.3    |        0.9265 |       0.0133 | classic   |
| RA_Consensus                       |     7.5333 |        0.9271 |       0.0112 | proposed  |
| RA_noRF                            |     8.2    |        0.9265 |       0.0113 | proposed  |
| RA_noRed                           |    10.6    |        0.9228 |       0.0122 | proposed  |
| STD_ANOVA                          |    11.8667 |        0.907  |       0.0346 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=4.303): WITHOUT_FS, P4_Inter_IntraWeight_Adjustment_FS, F0_Fuzzy_RAR, RA_mean, SOTA_SHAP_XGB

### Average ranks: KNN__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| P4_Inter_IntraWeight_Adjustment_FS |        2.1 |        0.9248 |       0.0063 | proposed  |
| WITHOUT_FS                         |        2.6 |        0.9195 |       0      | no_fs     |
| STD_MI                             |        3.6 |        0.9191 |       0      | classic   |
| SOTA_mRMR                          |        4.8 |        0.9164 |       0.006  | benchmark |
| F0_Fuzzy_RAR                       |        4.9 |        0.9155 |       0.0006 | proposed  |
| RA_mean                            |        5.4 |        0.9154 |       0.0042 | proposed  |
| RA_Consensus                       |        7.6 |        0.9121 |       0.0021 | proposed  |
| RA_noRF                            |        7.6 |        0.9113 |       0.0031 | proposed  |
| SOTA_SHAP_XGB                      |        7.8 |        0.9115 |       0.0068 | benchmark |
| STD_RFE_RF                         |        9.2 |        0.9085 |       0.0022 | classic   |
| RA_noRed                           |       10.4 |        0.9064 |       0.0017 | proposed  |
| STD_ANOVA                          |       12   |        0.8667 |       0.0337 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=7.452): P4_Inter_IntraWeight_Adjustment_FS, WITHOUT_FS, STD_MI, SOTA_mRMR, F0_Fuzzy_RAR, RA_mean, RA_Consensus, RA_noRF, SOTA_SHAP_XGB, STD_RFE_RF

### Average ranks: RF__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |        1   |        0.9417 |       0.0005 | no_fs     |
| SOTA_SHAP_XGB                      |        2.6 |        0.937  |       0.0025 | benchmark |
| F0_Fuzzy_RAR                       |        4   |        0.9352 |       0.0009 | proposed  |
| RA_mean                            |        5.1 |        0.9352 |       0.0027 | proposed  |
| STD_RFE_RF                         |        5.2 |        0.9347 |       0.0016 | classic   |
| P4_Inter_IntraWeight_Adjustment_FS |        6.2 |        0.9337 |       0.002  | proposed  |
| RA_Consensus                       |        7.2 |        0.9332 |       0.0017 | proposed  |
| STD_MI                             |        7.3 |        0.933  |       0.0007 | classic   |
| SOTA_mRMR                          |        8.2 |        0.9332 |       0.0012 | benchmark |
| RA_noRF                            |        9   |        0.9325 |       0.0012 | proposed  |
| RA_noRed                           |       10.4 |        0.9302 |       0.0028 | proposed  |
| STD_ANOVA                          |       11.8 |        0.9261 |       0.0026 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=7.452): WITHOUT_FS, SOTA_SHAP_XGB, F0_Fuzzy_RAR, RA_mean, STD_RFE_RF, P4_Inter_IntraWeight_Adjustment_FS, RA_Consensus, STD_MI, SOTA_mRMR

### Average ranks: XGB__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |        1   |        0.943  |       0.001  | no_fs     |
| P4_Inter_IntraWeight_Adjustment_FS |        4   |        0.9378 |       0.0015 | proposed  |
| RA_mean                            |        4.2 |        0.9382 |       0.0018 | proposed  |
| F0_Fuzzy_RAR                       |        4.4 |        0.9377 |       0.0006 | proposed  |
| SOTA_mRMR                          |        5.2 |        0.9375 |       0.0003 | benchmark |
| SOTA_SHAP_XGB                      |        6.3 |        0.9374 |       0.0011 | benchmark |
| STD_MI                             |        6.8 |        0.9372 |       0.0006 | classic   |
| STD_RFE_RF                         |        7.5 |        0.9362 |       0.0018 | classic   |
| RA_Consensus                       |        7.8 |        0.9361 |       0.0015 | proposed  |
| RA_noRF                            |        8   |        0.9356 |       0.0018 | proposed  |
| RA_noRed                           |       11   |        0.9317 |       0.003  | proposed  |
| STD_ANOVA                          |       11.8 |        0.9282 |       0.0009 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=7.452): WITHOUT_FS, P4_Inter_IntraWeight_Adjustment_FS, RA_mean, F0_Fuzzy_RAR, SOTA_mRMR, SOTA_SHAP_XGB, STD_MI, STD_RFE_RF, RA_Consensus, RA_noRF

## Wilcoxon + Holm: proposed selectors vs the strongest competitors (pooled all-model scope if available)

| ref                                | other                              |   n_blocks |   mean_diff |   p_value |   p_holm | verdict                   |
|:-----------------------------------|:-----------------------------------|-----------:|------------:|----------:|---------:|:--------------------------|
| RA_Consensus                       | F0_Fuzzy_RAR                       |         15 |    -0.00233 |   0.00018 |  0.00146 | ref worse                 |
| RA_Consensus                       | P4_Inter_IntraWeight_Adjustment_FS |         15 |    -0.00497 |   0.00262 |  0.01575 | ref worse                 |
| RA_Consensus                       | RA_mean                            |         15 |    -0.00248 |   0.00201 |  0.0141  | ref worse                 |
| RA_Consensus                       | SOTA_mRMR                          |         15 |    -0.00192 |   0.10699 |  0.42798 | no significant difference |
| RA_Consensus                       | STD_MI                             |         15 |    -0.00264 |   0.02557 |  0.12787 | no significant difference |
| RA_Consensus                       | WITHOUT_FS                         |         15 |    -0.00763 |   6e-05   |  0.00067 | ref worse                 |
| RA_noRF                            | F0_Fuzzy_RAR                       |         15 |    -0.00295 |   0.00012 |  0.00122 | ref worse                 |
| RA_noRF                            | P4_Inter_IntraWeight_Adjustment_FS |         15 |    -0.00559 |   0.00061 |  0.00549 | ref worse                 |
| RA_noRF                            | RA_mean                            |         15 |    -0.0031  |   0.00153 |  0.00916 | ref worse                 |
| RA_noRF                            | SOTA_mRMR                          |         15 |    -0.00254 |   0.05001 |  0.20005 | no significant difference |
| RA_noRF                            | STD_MI                             |         15 |    -0.00326 |   0.00336 |  0.01678 | ref worse                 |
| RA_noRF                            | WITHOUT_FS                         |         15 |    -0.00826 |   0.00065 |  0.00549 | ref worse                 |
| RA_mean                            | F0_Fuzzy_RAR                       |         15 |     0.00015 |   0.73322 |  1       | no significant difference |
| RA_mean                            | P4_Inter_IntraWeight_Adjustment_FS |         15 |    -0.00249 |   0.35913 |  1       | no significant difference |
| RA_mean                            | SOTA_mRMR                          |         15 |     0.00056 |   0.33026 |  1       | no significant difference |
| RA_mean                            | STD_MI                             |         15 |    -0.00016 |   0.97495 |  1       | no significant difference |
| RA_mean                            | WITHOUT_FS                         |         15 |    -0.00516 |   0.0012  |  0.01083 | ref worse                 |
| RA_noRed                           | F0_Fuzzy_RAR                       |         15 |    -0.00665 |   0.00065 |  0.00366 | ref worse                 |
| RA_noRed                           | P4_Inter_IntraWeight_Adjustment_FS |         15 |    -0.00929 |   6e-05   |  0.00067 | ref worse                 |
| RA_noRed                           | RA_mean                            |         15 |    -0.0068  |   6e-05   |  0.00067 | ref worse                 |
| RA_noRed                           | SOTA_mRMR                          |         15 |    -0.00624 |   0.00031 |  0.00244 | ref worse                 |
| RA_noRed                           | STD_MI                             |         15 |    -0.00696 |   0.00065 |  0.00366 | ref worse                 |
| RA_noRed                           | WITHOUT_FS                         |         15 |    -0.01196 |   0.00065 |  0.00366 | ref worse                 |
| F0_Fuzzy_RAR                       | P4_Inter_IntraWeight_Adjustment_FS |         15 |    -0.00264 |   0.33042 |  1       | no significant difference |
| F0_Fuzzy_RAR                       | RA_mean                            |         15 |    -0.00015 |   0.73322 |  1       | no significant difference |
| F0_Fuzzy_RAR                       | SOTA_mRMR                          |         15 |     0.00041 |   0.1553  |  0.77651 | no significant difference |
| F0_Fuzzy_RAR                       | STD_MI                             |         15 |    -0.00031 |   0.56928 |  1       | no significant difference |
| F0_Fuzzy_RAR                       | WITHOUT_FS                         |         15 |    -0.00531 |   0.00064 |  0.00575 | ref worse                 |
| P4_Inter_IntraWeight_Adjustment_FS | F0_Fuzzy_RAR                       |         15 |     0.00264 |   0.33042 |  1       | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | RA_mean                            |         15 |     0.00249 |   0.35913 |  1       | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | SOTA_mRMR                          |         15 |     0.00305 |   0.25589 |  1       | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | STD_MI                             |         15 |     0.00233 |   0.07817 |  0.46903 | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | WITHOUT_FS                         |         15 |    -0.00267 |   0.15555 |  0.77776 | no significant difference |

Full table: wilcoxon_holm.csv (scope used above: ALL_MODELS__fold_level).

## Win / Tie / Loss (block level, tolerance 0.001)

Summed over every opponent (ALL_MODELS__fold_level):

| ref                                |   win |   tie |   loss |
|:-----------------------------------|------:|------:|-------:|
| F0_Fuzzy_RAR                       |    93 |    34 |     38 |
| P4_Inter_IntraWeight_Adjustment_FS |   103 |    25 |     37 |
| RA_Consensus                       |    55 |    26 |     84 |
| RA_mean                            |    87 |    34 |     44 |
| RA_noRF                            |    47 |    25 |     93 |
| RA_noRed                           |    14 |    15 |    136 |

Significance-level W/T/L across models (per-model Wilcoxon-Holm), by reference vs opponent group:

|                                                     |   sig_win |   sig_tie |   sig_loss |
|:----------------------------------------------------|----------:|----------:|-----------:|
| ('F0_Fuzzy_RAR', 'benchmark')                       |         0 |         6 |          0 |
| ('F0_Fuzzy_RAR', 'classic')                         |         0 |         9 |          0 |
| ('F0_Fuzzy_RAR', 'no_fs')                           |         0 |         3 |          0 |
| ('F0_Fuzzy_RAR', 'proposed')                        |         0 |        15 |          0 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'benchmark') |         0 |         6 |          0 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'classic')   |         0 |         9 |          0 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'no_fs')     |         0 |         3 |          0 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'proposed')  |         0 |        15 |          0 |
| ('RA_Consensus', 'benchmark')                       |         0 |         6 |          0 |
| ('RA_Consensus', 'classic')                         |         0 |         9 |          0 |
| ('RA_Consensus', 'no_fs')                           |         0 |         3 |          0 |
| ('RA_Consensus', 'proposed')                        |         0 |        15 |          0 |
| ('RA_mean', 'benchmark')                            |         0 |         6 |          0 |
| ('RA_mean', 'classic')                              |         0 |         9 |          0 |
| ('RA_mean', 'no_fs')                                |         0 |         3 |          0 |
| ('RA_mean', 'proposed')                             |         0 |        15 |          0 |
| ('RA_noRF', 'benchmark')                            |         0 |         6 |          0 |
| ('RA_noRF', 'classic')                              |         0 |         9 |          0 |
| ('RA_noRF', 'no_fs')                                |         0 |         3 |          0 |
| ('RA_noRF', 'proposed')                             |         0 |        15 |          0 |
| ('RA_noRed', 'benchmark')                           |         0 |         6 |          0 |
| ('RA_noRed', 'classic')                             |         0 |         9 |          0 |
| ('RA_noRed', 'no_fs')                               |         0 |         3 |          0 |
| ('RA_noRed', 'proposed')                            |         0 |        15 |          0 |
