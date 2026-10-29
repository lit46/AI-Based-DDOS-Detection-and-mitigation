# Statistical validation (metric: accuracy)

Interpretation notes
- 'Win/Tie/Loss' (your 'wintaylor's') is implemented as Win/Tie/Loss: Win = proposed accuracy higher by more than the tolerance (0.001), Tie = within tolerance, Loss = lower.
- Folds of one CV share training data and repeats reuse the same rows, so blocks are positively correlated; p-values are anti-conservative (Nadeau & Bengio 2003). Use them to rank methods, not as exact error rates.
- With n paired blocks the smallest two-sided Wilcoxon p is 2/2^n; n=5 repeats cannot go below 0.0625, so fold-level blocks (n = repeats x folds) are used.
- Holm correction is applied per (scope, reference method).

## Friedman + Iman-Davenport

| scope                    |   N |   k |     chi2 |   p_friedman |   F_iman_davenport |   df1 |   df2 |   p_iman_davenport |
|:-------------------------|----:|----:|---------:|-------------:|-------------------:|------:|------:|-------------------:|
| RF__fold_level           |  20 |  10 | 133.029  |      0       |            53.8111 |     9 |   171 |                  0 |
| XGB__fold_level          |  20 |  10 | 110.27   |      0       |            30.0467 |     9 |   171 |                  0 |
| ALL_MODELS__fold_level   |  40 |  10 | 216.025  |      0       |            58.5166 |     9 |   351 |                  0 |
| ALL_MODELS__repeat_level |   4 |  10 |  30.3273 |      0.00039 |            16.0385 |     9 |    27 |                  0 |

## Nemenyi critical difference

| scope                    |   k |   N |   alpha |   q_alpha_over_sqrt2 |   critical_difference |
|:-------------------------|----:|----:|--------:|---------------------:|----------------------:|
| RF__fold_level           |  10 |  20 |    0.05 |               3.1637 |                3.029  |
| XGB__fold_level          |  10 |  20 |    0.05 |               3.1637 |                3.029  |
| ALL_MODELS__fold_level   |  10 |  40 |    0.05 |               3.1637 |                2.1418 |
| ALL_MODELS__repeat_level |  10 |   4 |    0.05 |               3.1637 |                6.773  |

### Average ranks: ALL_MODELS__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |     1.05   |        0.9323 |       0.0049 | no_fs     |
| STD_RFE_RF                         |     4.0875 |        0.9265 |       0.0063 | classic   |
| SOTA_SHAP_XGB                      |     4.2125 |        0.9262 |       0.0078 | benchmark |
| F0_Fuzzy_RAR                       |     4.6    |        0.9261 |       0.0061 | proposed  |
| P4_Inter_IntraWeight_Adjustment_FS |     4.7625 |        0.9263 |       0.0052 | proposed  |
| STD_MI                             |     5.85   |        0.925  |       0.0065 | classic   |
| SOTA_mRMR                          |     6.0875 |        0.9246 |       0.0072 | benchmark |
| CR_Fuzzy_RAR                       |     6.975  |        0.9197 |       0.0108 | proposed  |
| CR_noAssoc                         |     7.775  |        0.9155 |       0.012  | proposed  |
| STD_ANOVA                          |     9.6    |        0.9022 |       0.0168 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=2.142): WITHOUT_FS

### Average ranks: ALL_MODELS__repeat_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |       1    |        0.9323 |       0.0007 | no_fs     |
| STD_RFE_RF                         |       3    |        0.9265 |       0.0028 | classic   |
| P4_Inter_IntraWeight_Adjustment_FS |       3.75 |        0.9263 |       0.0026 | proposed  |
| F0_Fuzzy_RAR                       |       4.75 |        0.9261 |       0.0028 | proposed  |
| SOTA_mRMR                          |       4.75 |        0.9246 |       0.0049 | benchmark |
| SOTA_SHAP_XGB                      |       5.25 |        0.9262 |       0.0022 | benchmark |
| STD_MI                             |       5.5  |        0.925  |       0.0041 | classic   |
| CR_Fuzzy_RAR                       |       8    |        0.9197 |       0.0016 | proposed  |
| CR_noAssoc                         |       9    |        0.9155 |       0.0028 | proposed  |
| STD_ANOVA                          |      10    |        0.9022 |       0.007  | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=6.773): WITHOUT_FS, STD_RFE_RF, P4_Inter_IntraWeight_Adjustment_FS, F0_Fuzzy_RAR, SOTA_mRMR, SOTA_SHAP_XGB, STD_MI

### Average ranks: RF__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |      1     |        0.9318 |       0.0049 | no_fs     |
| SOTA_SHAP_XGB                      |      2.85  |        0.9247 |       0.0096 | benchmark |
| STD_RFE_RF                         |      3.725 |        0.9241 |       0.0068 | classic   |
| P4_Inter_IntraWeight_Adjustment_FS |      4.575 |        0.9241 |       0.0045 | proposed  |
| F0_Fuzzy_RAR                       |      4.6   |        0.9237 |       0.0064 | proposed  |
| CR_Fuzzy_RAR                       |      6.55  |        0.9184 |       0.0098 | proposed  |
| STD_MI                             |      6.85  |        0.9214 |       0.0063 | classic   |
| CR_noAssoc                         |      7.45  |        0.9135 |       0.0126 | proposed  |
| SOTA_mRMR                          |      7.8   |        0.9204 |       0.0068 | benchmark |
| STD_ANOVA                          |      9.6   |        0.8965 |       0.0217 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=3.029): WITHOUT_FS, SOTA_SHAP_XGB, STD_RFE_RF

### Average ranks: XGB__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |      1.1   |        0.9329 |       0.0049 | no_fs     |
| SOTA_mRMR                          |      4.375 |        0.9289 |       0.0047 | benchmark |
| STD_RFE_RF                         |      4.45  |        0.9289 |       0.0048 | classic   |
| F0_Fuzzy_RAR                       |      4.6   |        0.9286 |       0.0048 | proposed  |
| STD_MI                             |      4.85  |        0.9286 |       0.0047 | classic   |
| P4_Inter_IntraWeight_Adjustment_FS |      4.95  |        0.9286 |       0.005  | proposed  |
| SOTA_SHAP_XGB                      |      5.575 |        0.9278 |       0.0055 | benchmark |
| CR_Fuzzy_RAR                       |      7.4   |        0.921  |       0.0118 | proposed  |
| CR_noAssoc                         |      8.1   |        0.9175 |       0.0114 | proposed  |
| STD_ANOVA                          |      9.6   |        0.9079 |       0.0062 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=3.029): WITHOUT_FS

## Wilcoxon + Holm: proposed selectors vs the strongest competitors (pooled all-model scope if available)

| ref                                | other                              |   n_blocks |   mean_diff |   p_value |   p_holm | verdict                   |
|:-----------------------------------|:-----------------------------------|-----------:|------------:|----------:|---------:|:--------------------------|
| F0_Fuzzy_RAR                       | P4_Inter_IntraWeight_Adjustment_FS |         40 |    -0.0002  |   0.79324 |  0.79324 | no significant difference |
| F0_Fuzzy_RAR                       | SOTA_SHAP_XGB                      |         40 |    -0.00011 |   0.15061 |  0.30123 | no significant difference |
| F0_Fuzzy_RAR                       | STD_MI                             |         40 |     0.00114 |   3e-05   |  0.00013 | ref better                |
| F0_Fuzzy_RAR                       | STD_RFE_RF                         |         40 |    -0.00039 |   0.05651 |  0.16953 | no significant difference |
| F0_Fuzzy_RAR                       | WITHOUT_FS                         |         40 |    -0.00621 |   0       |  0       | ref worse                 |
| P4_Inter_IntraWeight_Adjustment_FS | F0_Fuzzy_RAR                       |         40 |     0.0002  |   0.79324 |  0.79324 | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | SOTA_SHAP_XGB                      |         40 |     9e-05   |   0.09182 |  0.27547 | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | STD_MI                             |         40 |     0.00134 |   0.0061  |  0.02588 | ref better                |
| P4_Inter_IntraWeight_Adjustment_FS | STD_RFE_RF                         |         40 |    -0.00019 |   0.32318 |  0.64636 | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | WITHOUT_FS                         |         40 |    -0.00601 |   0       |  0       | ref worse                 |
| CR_Fuzzy_RAR                       | F0_Fuzzy_RAR                       |         40 |    -0.00647 |   0       |  1e-05   | ref worse                 |
| CR_Fuzzy_RAR                       | P4_Inter_IntraWeight_Adjustment_FS |         40 |    -0.00667 |   0       |  1e-05   | ref worse                 |
| CR_Fuzzy_RAR                       | SOTA_SHAP_XGB                      |         40 |    -0.00658 |   0       |  1e-05   | ref worse                 |
| CR_Fuzzy_RAR                       | STD_MI                             |         40 |    -0.00533 |   0.00251 |  0.00754 | ref worse                 |
| CR_Fuzzy_RAR                       | STD_RFE_RF                         |         40 |    -0.00686 |   0       |  0       | ref worse                 |
| CR_Fuzzy_RAR                       | WITHOUT_FS                         |         40 |    -0.01268 |   0       |  0       | ref worse                 |
| CR_noAssoc                         | F0_Fuzzy_RAR                       |         40 |    -0.01066 |   0       |  1e-05   | ref worse                 |
| CR_noAssoc                         | P4_Inter_IntraWeight_Adjustment_FS |         40 |    -0.01086 |   0       |  1e-05   | ref worse                 |
| CR_noAssoc                         | SOTA_SHAP_XGB                      |         40 |    -0.01077 |   0       |  0       | ref worse                 |
| CR_noAssoc                         | STD_MI                             |         40 |    -0.00953 |   1e-05   |  4e-05   | ref worse                 |
| CR_noAssoc                         | STD_RFE_RF                         |         40 |    -0.01106 |   0       |  0       | ref worse                 |
| CR_noAssoc                         | WITHOUT_FS                         |         40 |    -0.01687 |   0       |  0       | ref worse                 |

Full table: wilcoxon_holm.csv (scope used above: ALL_MODELS__fold_level).

## Win / Tie / Loss (block level, tolerance 0.001)

Summed over every opponent (ALL_MODELS__fold_level):

| ref                                |   win |   tie |   loss |
|:-----------------------------------|------:|------:|-------:|
| CR_Fuzzy_RAR                       |    80 |    74 |    206 |
| CR_noAssoc                         |    59 |    65 |    236 |
| F0_Fuzzy_RAR                       |   164 |   102 |     94 |
| P4_Inter_IntraWeight_Adjustment_FS |   169 |    80 |    111 |

Significance-level W/T/L across models (per-model Wilcoxon-Holm), by reference vs opponent group:

|                                                     |   sig_win |   sig_tie |   sig_loss |
|:----------------------------------------------------|----------:|----------:|-----------:|
| ('CR_Fuzzy_RAR', 'benchmark')                       |         0 |         1 |          3 |
| ('CR_Fuzzy_RAR', 'classic')                         |         2 |         1 |          3 |
| ('CR_Fuzzy_RAR', 'no_fs')                           |         0 |         0 |          2 |
| ('CR_Fuzzy_RAR', 'proposed')                        |         0 |         2 |          4 |
| ('CR_noAssoc', 'benchmark')                         |         0 |         1 |          3 |
| ('CR_noAssoc', 'classic')                           |         2 |         0 |          4 |
| ('CR_noAssoc', 'no_fs')                             |         0 |         0 |          2 |
| ('CR_noAssoc', 'proposed')                          |         0 |         2 |          4 |
| ('F0_Fuzzy_RAR', 'benchmark')                       |         1 |         2 |          1 |
| ('F0_Fuzzy_RAR', 'classic')                         |         3 |         3 |          0 |
| ('F0_Fuzzy_RAR', 'no_fs')                           |         0 |         0 |          2 |
| ('F0_Fuzzy_RAR', 'proposed')                        |         4 |         2 |          0 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'benchmark') |         1 |         2 |          1 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'classic')   |         3 |         3 |          0 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'no_fs')     |         0 |         0 |          2 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'proposed')  |         4 |         2 |          0 |
