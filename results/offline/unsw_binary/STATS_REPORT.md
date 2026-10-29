# Statistical validation (metric: accuracy)

Interpretation notes
- 'Win/Tie/Loss' (your 'wintaylor's') is implemented as Win/Tie/Loss: Win = proposed accuracy higher by more than the tolerance (0.001), Tie = within tolerance, Loss = lower.
- Folds of one CV share training data and repeats reuse the same rows, so blocks are positively correlated; p-values are anti-conservative (Nadeau & Bengio 2003). Use them to rank methods, not as exact error rates.
- With n paired blocks the smallest two-sided Wilcoxon p is 2/2^n; n=5 repeats cannot go below 0.0625, so fold-level blocks (n = repeats x folds) are used.
- Holm correction is applied per (scope, reference method).

## Friedman + Iman-Davenport

| scope                    |   N |   k |    chi2 |   p_friedman |   F_iman_davenport |   df1 |   df2 |   p_iman_davenport |
|:-------------------------|----:|----:|--------:|-------------:|-------------------:|------:|------:|-------------------:|
| KNN__fold_level          |  10 |  18 | 130.173 |            0 |            29.4161 |    17 |   153 |                  0 |
| RF__fold_level           |  10 |  18 | 138.204 |            0 |            39.1185 |    17 |   153 |                  0 |
| XGB__fold_level          |  10 |  18 | 137.111 |            0 |            37.5198 |    17 |   153 |                  0 |
| ALL_MODELS__fold_level   |  30 |  18 | 305.915 |            0 |            43.4697 |    17 |   493 |                  0 |
| ALL_MODELS__repeat_level |  30 |  18 | 305.915 |            0 |            43.4697 |    17 |   493 |                  0 |

## Nemenyi critical difference

| scope                    |   k |   N |   alpha |   q_alpha_over_sqrt2 |   critical_difference |
|:-------------------------|----:|----:|--------:|---------------------:|----------------------:|
| KNN__fold_level          |  18 |  10 |    0.05 |               3.4887 |                8.3291 |
| RF__fold_level           |  18 |  10 |    0.05 |               3.4887 |                8.3291 |
| XGB__fold_level          |  18 |  10 |    0.05 |               3.4887 |                8.3291 |
| ALL_MODELS__fold_level   |  18 |  30 |    0.05 |               3.4887 |                4.8088 |
| ALL_MODELS__repeat_level |  18 |  30 |    0.05 |               3.4887 |                4.8088 |

### Average ranks: ALL_MODELS__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| STD_MI                             |     3.0167 |        0.8688 |       0.0059 | classic   |
| SOTA_mRMR                          |     4.9333 |        0.864  |       0.0082 | benchmark |
| SOTA_ReliefF                       |     6.3    |        0.8655 |       0.0042 | benchmark |
| P1_New_Fuzzy_Rule_FS               |     6.5167 |        0.8616 |       0.0108 | proposed  |
| F0_Fuzzy_RAR                       |     6.9    |        0.8632 |       0.006  | proposed  |
| CR_randomFolds                     |     6.9833 |        0.8635 |       0.0059 | proposed  |
| STD_RFE_RF                         |     7.25   |        0.8609 |       0.0097 | classic   |
| P4_Inter_IntraWeight_Adjustment_FS |     7.2667 |        0.8635 |       0.0058 | proposed  |
| SOTA_CMIM                          |     7.4667 |        0.8612 |       0.0097 | benchmark |
| SOTA_JMIM                          |     7.9333 |        0.8648 |       0.0066 | benchmark |
| WITHOUT_FS                         |     9.4333 |        0.857  |       0.014  | no_fs     |
| SOTA_SHAP_XGB                      |    10.2    |        0.8565 |       0.0131 | benchmark |
| CR_noSpread                        |    11.0333 |        0.8553 |       0.0122 | proposed  |
| CR_Fuzzy_RAR                       |    12.1    |        0.8505 |       0.0146 | proposed  |
| CR_noAssoc                         |    14.7    |        0.8196 |       0.0849 | proposed  |
| CR_noRed                           |    15.0333 |        0.8155 |       0.0856 | proposed  |
| STD_ANOVA                          |    16.9333 |        0.809  |       0.034  | classic   |
| STD_CHI2                           |    17      |        0.7997 |       0.0363 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=4.809): STD_MI, SOTA_mRMR, SOTA_ReliefF, P1_New_Fuzzy_Rule_FS, F0_Fuzzy_RAR, CR_randomFolds, STD_RFE_RF, P4_Inter_IntraWeight_Adjustment_FS, SOTA_CMIM

### Average ranks: ALL_MODELS__repeat_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| STD_MI                             |     3.0167 |        0.8688 |       0.0059 | classic   |
| SOTA_mRMR                          |     4.9333 |        0.864  |       0.0082 | benchmark |
| SOTA_ReliefF                       |     6.3    |        0.8655 |       0.0042 | benchmark |
| P1_New_Fuzzy_Rule_FS               |     6.5167 |        0.8616 |       0.0108 | proposed  |
| F0_Fuzzy_RAR                       |     6.9    |        0.8632 |       0.006  | proposed  |
| CR_randomFolds                     |     6.9833 |        0.8635 |       0.0059 | proposed  |
| STD_RFE_RF                         |     7.25   |        0.8609 |       0.0097 | classic   |
| P4_Inter_IntraWeight_Adjustment_FS |     7.2667 |        0.8635 |       0.0058 | proposed  |
| SOTA_CMIM                          |     7.4667 |        0.8612 |       0.0097 | benchmark |
| SOTA_JMIM                          |     7.9333 |        0.8648 |       0.0066 | benchmark |
| WITHOUT_FS                         |     9.4333 |        0.857  |       0.014  | no_fs     |
| SOTA_SHAP_XGB                      |    10.2    |        0.8565 |       0.0131 | benchmark |
| CR_noSpread                        |    11.0333 |        0.8553 |       0.0122 | proposed  |
| CR_Fuzzy_RAR                       |    12.1    |        0.8505 |       0.0146 | proposed  |
| CR_noAssoc                         |    14.7    |        0.8196 |       0.0849 | proposed  |
| CR_noRed                           |    15.0333 |        0.8155 |       0.0856 | proposed  |
| STD_ANOVA                          |    16.9333 |        0.809  |       0.034  | classic   |
| STD_CHI2                           |    17      |        0.7997 |       0.0363 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=4.809): STD_MI, SOTA_mRMR, SOTA_ReliefF, P1_New_Fuzzy_Rule_FS, F0_Fuzzy_RAR, CR_randomFolds, STD_RFE_RF, P4_Inter_IntraWeight_Adjustment_FS, SOTA_CMIM

### Average ranks: KNN__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| STD_MI                             |       1.05 |        0.8712 |       0      | classic   |
| SOTA_ReliefF                       |       3    |        0.8663 |       0.0021 | benchmark |
| SOTA_JMIM                          |       3.2  |        0.8669 |       0.0055 | benchmark |
| CR_randomFolds                     |       6.1  |        0.8593 |       0.0035 | proposed  |
| P4_Inter_IntraWeight_Adjustment_FS |       6.3  |        0.8593 |       0.0039 | proposed  |
| F0_Fuzzy_RAR                       |       6.5  |        0.8584 |       0.0028 | proposed  |
| SOTA_mRMR                          |       8.4  |        0.8554 |       0.0017 | benchmark |
| P1_New_Fuzzy_Rule_FS               |       8.95 |        0.8524 |       0.0123 | proposed  |
| CR_Fuzzy_RAR                       |       9.4  |        0.85   |       0.011  | proposed  |
| CR_noSpread                        |       9.6  |        0.8525 |       0.0078 | proposed  |
| SOTA_CMIM                          |       9.7  |        0.8518 |       0.0066 | benchmark |
| STD_RFE_RF                         |      10.5  |        0.8498 |       0.0046 | classic   |
| SOTA_SHAP_XGB                      |      12.1  |        0.8424 |       0.01   | benchmark |
| CR_noRed                           |      13.5  |        0.7772 |       0.1399 | proposed  |
| CR_noAssoc                         |      13.7  |        0.7794 |       0.1387 | proposed  |
| WITHOUT_FS                         |      14.8  |        0.8376 |       0      | no_fs     |
| STD_CHI2                           |      17.1  |        0.7504 |       0.0055 | classic   |
| STD_ANOVA                          |      17.1  |        0.7676 |       0.0242 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=8.329): STD_MI, SOTA_ReliefF, SOTA_JMIM, CR_randomFolds, P4_Inter_IntraWeight_Adjustment_FS, F0_Fuzzy_RAR, SOTA_mRMR, P1_New_Fuzzy_Rule_FS

### Average ranks: RF__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| SOTA_mRMR                          |        1.8 |        0.8746 |       0.0012 | benchmark |
| STD_MI                             |        1.9 |        0.8743 |       0.0003 | classic   |
| SOTA_CMIM                          |        4.4 |        0.8724 |       0.0032 | benchmark |
| STD_RFE_RF                         |        5.2 |        0.8722 |       0.0012 | classic   |
| P1_New_Fuzzy_Rule_FS               |        6   |        0.8716 |       0.0024 | proposed  |
| F0_Fuzzy_RAR                       |        7   |        0.8712 |       0.0005 | proposed  |
| CR_randomFolds                     |        7.3 |        0.8712 |       0.0005 | proposed  |
| SOTA_SHAP_XGB                      |        8.5 |        0.8703 |       0.0025 | benchmark |
| P4_Inter_IntraWeight_Adjustment_FS |        8.7 |        0.8707 |       0.0014 | proposed  |
| SOTA_JMIM                          |        8.9 |        0.8704 |       0.0016 | benchmark |
| SOTA_ReliefF                       |       10.1 |        0.8698 |       0.0005 | benchmark |
| CR_noSpread                        |       11.2 |        0.8656 |       0.0059 | proposed  |
| CR_Fuzzy_RAR                       |       12.4 |        0.8628 |       0.0055 | proposed  |
| WITHOUT_FS                         |       12.5 |        0.8678 |       0.0005 | no_fs     |
| CR_noAssoc                         |       15.4 |        0.8481 |       0.0281 | proposed  |
| CR_noRed                           |       15.5 |        0.8449 |       0.0326 | proposed  |
| STD_CHI2                           |       17.1 |        0.8319 |       0.005  | classic   |
| STD_ANOVA                          |       17.1 |        0.8388 |       0.0086 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=8.329): SOTA_mRMR, STD_MI, SOTA_CMIM, STD_RFE_RF, P1_New_Fuzzy_Rule_FS, F0_Fuzzy_RAR, CR_randomFolds, SOTA_SHAP_XGB, P4_Inter_IntraWeight_Adjustment_FS, SOTA_JMIM, SOTA_ReliefF

### Average ranks: XGB__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |       1    |        0.8656 |       0.0007 | no_fs     |
| P1_New_Fuzzy_Rule_FS               |       4.6  |        0.8608 |       0.0037 | proposed  |
| SOTA_mRMR                          |       4.6  |        0.862  |       0.0016 | benchmark |
| SOTA_ReliefF                       |       5.8  |        0.8605 |       0.0014 | benchmark |
| STD_RFE_RF                         |       6.05 |        0.8607 |       0.0013 | classic   |
| STD_MI                             |       6.1  |        0.8608 |       0.0014 | classic   |
| P4_Inter_IntraWeight_Adjustment_FS |       6.8  |        0.8604 |       0.0015 | proposed  |
| F0_Fuzzy_RAR                       |       7.2  |        0.8602 |       0.0006 | proposed  |
| CR_randomFolds                     |       7.55 |        0.86   |       0.0009 | proposed  |
| SOTA_CMIM                          |       8.3  |        0.8594 |       0.0026 | benchmark |
| SOTA_SHAP_XGB                      |      10    |        0.8567 |       0.004  | benchmark |
| SOTA_JMIM                          |      11.7  |        0.857  |       0.001  | benchmark |
| CR_noSpread                        |      12.3  |        0.8476 |       0.0138 | proposed  |
| CR_Fuzzy_RAR                       |      14.5  |        0.8386 |       0.0145 | proposed  |
| CR_noAssoc                         |      15    |        0.8312 |       0.0189 | proposed  |
| CR_noRed                           |      16.1  |        0.8246 |       0.0175 | proposed  |
| STD_ANOVA                          |      16.6  |        0.8205 |       0.0053 | classic   |
| STD_CHI2                           |      16.8  |        0.817  |       0.0027 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=8.329): WITHOUT_FS, P1_New_Fuzzy_Rule_FS, SOTA_mRMR, SOTA_ReliefF, STD_RFE_RF, STD_MI, P4_Inter_IntraWeight_Adjustment_FS, F0_Fuzzy_RAR, CR_randomFolds, SOTA_CMIM

## Wilcoxon + Holm: proposed selectors vs the strongest competitors (pooled all-model scope if available)

| ref                                | other                              |   n_blocks |   mean_diff |   p_value |   p_holm | verdict                   |
|:-----------------------------------|:-----------------------------------|-----------:|------------:|----------:|---------:|:--------------------------|
| F0_Fuzzy_RAR                       | CR_randomFolds                     |         30 |    -0.00026 |   0.29042 |  1       | no significant difference |
| F0_Fuzzy_RAR                       | P4_Inter_IntraWeight_Adjustment_FS |         30 |    -0.00022 |   0.82095 |  1       | no significant difference |
| F0_Fuzzy_RAR                       | SOTA_JMIM                          |         30 |    -0.00155 |   0.90177 |  1       | no significant difference |
| F0_Fuzzy_RAR                       | SOTA_ReliefF                       |         30 |    -0.00229 |   0.08204 |  0.69049 | no significant difference |
| F0_Fuzzy_RAR                       | SOTA_mRMR                          |         30 |    -0.00076 |   0.07672 |  0.69049 | no significant difference |
| F0_Fuzzy_RAR                       | STD_MI                             |         30 |    -0.00552 |   1e-05   |  0.00011 | ref worse                 |
| F0_Fuzzy_RAR                       | WITHOUT_FS                         |         30 |     0.00623 |   0.10168 |  0.71173 | no significant difference |
| P1_New_Fuzzy_Rule_FS               | CR_randomFolds                     |         30 |    -0.00192 |   0.95153 |  1       | no significant difference |
| P1_New_Fuzzy_Rule_FS               | P4_Inter_IntraWeight_Adjustment_FS |         30 |    -0.00188 |   0.64351 |  1       | no significant difference |
| P1_New_Fuzzy_Rule_FS               | SOTA_JMIM                          |         30 |    -0.00321 |   0.42245 |  1       | no significant difference |
| P1_New_Fuzzy_Rule_FS               | SOTA_ReliefF                       |         30 |    -0.00395 |   0.33874 |  1       | no significant difference |
| P1_New_Fuzzy_Rule_FS               | SOTA_mRMR                          |         30 |    -0.00242 |   0.05982 |  0.5384  | no significant difference |
| P1_New_Fuzzy_Rule_FS               | STD_MI                             |         30 |    -0.00718 |   0.00101 |  0.01216 | ref worse                 |
| P1_New_Fuzzy_Rule_FS               | WITHOUT_FS                         |         30 |     0.00457 |   0.07324 |  0.58595 | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | CR_randomFolds                     |         30 |    -4e-05   |   0.99179 |  1       | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | SOTA_JMIM                          |         30 |    -0.00133 |   0.99179 |  1       | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | SOTA_ReliefF                       |         30 |    -0.00207 |   0.07164 |  0.57312 | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | SOTA_mRMR                          |         30 |    -0.00054 |   0.38201 |  1       | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | STD_MI                             |         30 |    -0.0053  |   3e-05   |  0.0003  | ref worse                 |
| P4_Inter_IntraWeight_Adjustment_FS | WITHOUT_FS                         |         30 |     0.00645 |   0.04916 |  0.44245 | no significant difference |
| CR_Fuzzy_RAR                       | CR_randomFolds                     |         30 |    -0.01306 |   0       |  3e-05   | ref worse                 |
| CR_Fuzzy_RAR                       | P4_Inter_IntraWeight_Adjustment_FS |         30 |    -0.01302 |   0       |  3e-05   | ref worse                 |
| CR_Fuzzy_RAR                       | SOTA_JMIM                          |         30 |    -0.01435 |   0       |  1e-05   | ref worse                 |
| CR_Fuzzy_RAR                       | SOTA_ReliefF                       |         30 |    -0.01508 |   0       |  0       | ref worse                 |
| CR_Fuzzy_RAR                       | SOTA_mRMR                          |         30 |    -0.01355 |   0       |  3e-05   | ref worse                 |
| CR_Fuzzy_RAR                       | STD_MI                             |         30 |    -0.01832 |   0       |  0       | ref worse                 |
| CR_Fuzzy_RAR                       | WITHOUT_FS                         |         30 |    -0.00657 |   0.12413 |  0.16065 | no significant difference |
| CR_noSpread                        | CR_randomFolds                     |         30 |    -0.00825 |   9e-05   |  0.00089 | ref worse                 |
| CR_noSpread                        | P4_Inter_IntraWeight_Adjustment_FS |         30 |    -0.00821 |   0.00012 |  0.00111 | ref worse                 |
| CR_noSpread                        | SOTA_JMIM                          |         30 |    -0.00954 |   0.00026 |  0.00183 | ref worse                 |
| CR_noSpread                        | SOTA_ReliefF                       |         30 |    -0.01028 |   0       |  0       | ref worse                 |
| CR_noSpread                        | SOTA_mRMR                          |         30 |    -0.00875 |   0.00019 |  0.00151 | ref worse                 |
| CR_noSpread                        | STD_MI                             |         30 |    -0.01351 |   0       |  0       | ref worse                 |
| CR_noSpread                        | WITHOUT_FS                         |         30 |    -0.00176 |   0.71513 |  0.90433 | no significant difference |
| CR_randomFolds                     | P4_Inter_IntraWeight_Adjustment_FS |         30 |     4e-05   |   0.99179 |  1       | no significant difference |
| CR_randomFolds                     | SOTA_JMIM                          |         30 |    -0.00129 |   0.92625 |  1       | no significant difference |
| CR_randomFolds                     | SOTA_ReliefF                       |         30 |    -0.00202 |   0.05186 |  0.46671 | no significant difference |
| CR_randomFolds                     | SOTA_mRMR                          |         30 |    -0.00049 |   0.20589 |  1       | no significant difference |
| CR_randomFolds                     | STD_MI                             |         30 |    -0.00526 |   1e-05   |  6e-05   | ref worse                 |
| CR_randomFolds                     | WITHOUT_FS                         |         30 |     0.00649 |   0.08203 |  0.65623 | no significant difference |
| CR_noAssoc                         | CR_randomFolds                     |         30 |    -0.04393 |   0       |  0       | ref worse                 |
| CR_noAssoc                         | P4_Inter_IntraWeight_Adjustment_FS |         30 |    -0.04389 |   0       |  2e-05   | ref worse                 |
| CR_noAssoc                         | SOTA_JMIM                          |         30 |    -0.04522 |   0       |  0       | ref worse                 |
| CR_noAssoc                         | SOTA_ReliefF                       |         30 |    -0.04596 |   0       |  0       | ref worse                 |
| CR_noAssoc                         | SOTA_mRMR                          |         30 |    -0.04443 |   0       |  0       | ref worse                 |
| CR_noAssoc                         | STD_MI                             |         30 |    -0.04919 |   0       |  0       | ref worse                 |
| CR_noAssoc                         | WITHOUT_FS                         |         30 |    -0.03744 |   0.00046 |  0.00184 | ref worse                 |
| CR_noRed                           | CR_randomFolds                     |         30 |    -0.04797 |   0       |  0       | ref worse                 |
| CR_noRed                           | P4_Inter_IntraWeight_Adjustment_FS |         30 |    -0.04792 |   0       |  0       | ref worse                 |
| CR_noRed                           | SOTA_JMIM                          |         30 |    -0.04925 |   0       |  0       | ref worse                 |
| CR_noRed                           | SOTA_ReliefF                       |         30 |    -0.04999 |   0       |  2e-05   | ref worse                 |
| CR_noRed                           | SOTA_mRMR                          |         30 |    -0.04846 |   0       |  0       | ref worse                 |
| CR_noRed                           | STD_MI                             |         30 |    -0.05323 |   0       |  2e-05   | ref worse                 |
| CR_noRed                           | WITHOUT_FS                         |         30 |    -0.04147 |   0.00022 |  0.00111 | ref worse                 |

Full table: wilcoxon_holm.csv (scope used above: ALL_MODELS__fold_level).

## Win / Tie / Loss (block level, tolerance 0.001)

Summed over every opponent (ALL_MODELS__fold_level):

| ref                                |   win |   tie |   loss |
|:-----------------------------------|------:|------:|-------:|
| CR_Fuzzy_RAR                       |   154 |    31 |    325 |
| CR_noAssoc                         |    91 |    20 |    399 |
| CR_noRed                           |    82 |    15 |    413 |
| CR_noSpread                        |   184 |    46 |    280 |
| CR_randomFolds                     |   285 |    86 |    139 |
| F0_Fuzzy_RAR                       |   289 |    84 |    137 |
| P1_New_Fuzzy_Rule_FS               |   313 |    52 |    145 |
| P4_Inter_IntraWeight_Adjustment_FS |   290 |    78 |    142 |

Significance-level W/T/L across models (per-model Wilcoxon-Holm), by reference vs opponent group:

|                                                     |   sig_win |   sig_tie |   sig_loss |
|:----------------------------------------------------|----------:|----------:|-----------:|
| ('CR_Fuzzy_RAR', 'benchmark')                       |         0 |         8 |          7 |
| ('CR_Fuzzy_RAR', 'classic')                         |         6 |         1 |          5 |
| ('CR_Fuzzy_RAR', 'no_fs')                           |         0 |         2 |          1 |
| ('CR_Fuzzy_RAR', 'proposed')                        |         2 |        12 |          7 |
| ('CR_noAssoc', 'benchmark')                         |         0 |         5 |         10 |
| ('CR_noAssoc', 'classic')                           |         0 |         7 |          5 |
| ('CR_noAssoc', 'no_fs')                             |         0 |         1 |          2 |
| ('CR_noAssoc', 'proposed')                          |         0 |        11 |         10 |
| ('CR_noRed', 'benchmark')                           |         0 |         4 |         11 |
| ('CR_noRed', 'classic')                             |         0 |         7 |          5 |
| ('CR_noRed', 'no_fs')                               |         0 |         1 |          2 |
| ('CR_noRed', 'proposed')                            |         0 |        12 |          9 |
| ('CR_noSpread', 'benchmark')                        |         0 |        10 |          5 |
| ('CR_noSpread', 'classic')                          |         6 |         2 |          4 |
| ('CR_noSpread', 'no_fs')                            |         1 |         1 |          1 |
| ('CR_noSpread', 'proposed')                         |         1 |        16 |          4 |
| ('CR_randomFolds', 'benchmark')                     |         3 |        10 |          2 |
| ('CR_randomFolds', 'classic')                       |         7 |         3 |          2 |
| ('CR_randomFolds', 'no_fs')                         |         2 |         0 |          1 |
| ('CR_randomFolds', 'proposed')                      |         8 |        13 |          0 |
| ('F0_Fuzzy_RAR', 'benchmark')                       |         2 |        11 |          2 |
| ('F0_Fuzzy_RAR', 'classic')                         |         7 |         3 |          2 |
| ('F0_Fuzzy_RAR', 'no_fs')                           |         2 |         0 |          1 |
| ('F0_Fuzzy_RAR', 'proposed')                        |         7 |        14 |          0 |
| ('P1_New_Fuzzy_Rule_FS', 'benchmark')               |         0 |        15 |          0 |
| ('P1_New_Fuzzy_Rule_FS', 'classic')                 |         6 |         5 |          1 |
| ('P1_New_Fuzzy_Rule_FS', 'no_fs')                   |         0 |         2 |          1 |
| ('P1_New_Fuzzy_Rule_FS', 'proposed')                |         7 |        14 |          0 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'benchmark') |         1 |        12 |          2 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'classic')   |         7 |         3 |          2 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'no_fs')     |         2 |         0 |          1 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'proposed')  |         7 |        14 |          0 |
