# Statistical validation (metric: accuracy)

Interpretation notes
- 'Win/Tie/Loss' (your 'wintaylor's') is implemented as Win/Tie/Loss: Win = proposed accuracy higher by more than the tolerance (0.001), Tie = within tolerance, Loss = lower.
- Folds of one CV share training data and repeats reuse the same rows, so blocks are positively correlated; p-values are anti-conservative (Nadeau & Bengio 2003). Use them to rank methods, not as exact error rates.
- With n paired blocks the smallest two-sided Wilcoxon p is 2/2^n; n=5 repeats cannot go below 0.0625, so fold-level blocks (n = repeats x folds) are used.
- Holm correction is applied per (scope, reference method).

## Friedman + Iman-Davenport

| scope                    |   N |   k |     chi2 |   p_friedman |   F_iman_davenport |   df1 |   df2 |   p_iman_davenport |
|:-------------------------|----:|----:|---------:|-------------:|-------------------:|------:|------:|-------------------:|
| KNN__fold_level          |  30 |  12 |  66.5099 |            0 |            7.32015 |    11 |   319 |                  0 |
| RF__fold_level           |  30 |  12 | 103.039  |            0 |           13.1659  |    11 |   319 |                  0 |
| XGB__fold_level          |  30 |  12 |  86.8979 |            0 |           10.3662  |    11 |   319 |                  0 |
| ALL_MODELS__fold_level   |  90 |  12 | 208.137  |            0 |           23.6924  |    11 |   979 |                  0 |
| ALL_MODELS__repeat_level |   9 |  12 |  63.7009 |            0 |           14.4368  |    11 |    88 |                  0 |

## Nemenyi critical difference

| scope                    |   k |   N |   alpha |   q_alpha_over_sqrt2 |   critical_difference |
|:-------------------------|----:|----:|--------:|---------------------:|----------------------:|
| KNN__fold_level          |  12 |  30 |    0.05 |                3.268 |                3.0423 |
| RF__fold_level           |  12 |  30 |    0.05 |                3.268 |                3.0423 |
| XGB__fold_level          |  12 |  30 |    0.05 |                3.268 |                3.0423 |
| ALL_MODELS__fold_level   |  12 |  90 |    0.05 |                3.268 |                1.7565 |
| ALL_MODELS__repeat_level |  12 |   9 |    0.05 |                3.268 |                5.5545 |

### Average ranks: ALL_MODELS__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |     3.9778 |        0.9793 |       0.1079 | no_fs     |
| SOTA_SHAP_XGB                      |     4.7889 |        0.992  |       0.0455 | benchmark |
| RA_noRed                           |     5.0889 |        0.9988 |       0.0032 | proposed  |
| P4_Inter_IntraWeight_Adjustment_FS |     5.5333 |        0.9781 |       0.0769 | proposed  |
| STD_RFE_RF                         |     5.75   |        0.9987 |       0.0031 | classic   |
| STD_ANOVA                          |     6.4333 |        0.9677 |       0.0924 | classic   |
| F0_Fuzzy_RAR                       |     6.5111 |        0.9524 |       0.1486 | proposed  |
| RA_Consensus                       |     7.2444 |        0.968  |       0.0925 | proposed  |
| RA_mean                            |     7.7889 |        0.9482 |       0.1377 | proposed  |
| SOTA_mRMR                          |     8.05   |        0.9194 |       0.1898 | benchmark |
| RA_noRF                            |     8.3111 |        0.948  |       0.1376 | proposed  |
| STD_MI                             |     8.5222 |        0.9546 |       0.1247 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=1.756): WITHOUT_FS, SOTA_SHAP_XGB, RA_noRed, P4_Inter_IntraWeight_Adjustment_FS

### Average ranks: ALL_MODELS__repeat_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| STD_RFE_RF                         |     2.2222 |        0.9987 |       0.0003 | classic   |
| RA_noRed                           |     2.5556 |        0.9988 |       0.0003 | proposed  |
| SOTA_SHAP_XGB                      |     3.5556 |        0.992  |       0.0136 | benchmark |
| WITHOUT_FS                         |     4.3333 |        0.9793 |       0.0294 | no_fs     |
| P4_Inter_IntraWeight_Adjustment_FS |     5.5556 |        0.9781 |       0.0156 | proposed  |
| RA_Consensus                       |     6.8889 |        0.968  |       0.0001 | proposed  |
| STD_ANOVA                          |     7.1111 |        0.9677 |       0.0005 | classic   |
| F0_Fuzzy_RAR                       |     8.1111 |        0.9524 |       0.0334 | proposed  |
| STD_MI                             |     8.2222 |        0.9546 |       0.0258 | classic   |
| RA_mean                            |     8.5556 |        0.9482 |       0.0293 | proposed  |
| RA_noRF                            |     9.3333 |        0.948  |       0.0292 | proposed  |
| SOTA_mRMR                          |    11.5556 |        0.9194 |       0.0154 | benchmark |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=5.555): STD_RFE_RF, RA_noRed, SOTA_SHAP_XGB, WITHOUT_FS, P4_Inter_IntraWeight_Adjustment_FS, RA_Consensus, STD_ANOVA

### Average ranks: KNN__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |     4.3667 |        0.9401 |       0.1825 | no_fs     |
| SOTA_SHAP_XGB                      |     4.8333 |        0.9989 |       0.0031 | benchmark |
| STD_RFE_RF                         |     5.2167 |        0.9989 |       0.0031 | classic   |
| RA_noRed                           |     5.7    |        0.9986 |       0.0034 | proposed  |
| P4_Inter_IntraWeight_Adjustment_FS |     5.7167 |        0.9778 |       0.0778 | proposed  |
| F0_Fuzzy_RAR                       |     5.7833 |        0.94   |       0.1825 | proposed  |
| SOTA_mRMR                          |     6.6333 |        0.9399 |       0.1825 | benchmark |
| STD_ANOVA                          |     6.9    |        0.967  |       0.0933 | classic   |
| RA_Consensus                       |     7.05   |        0.968  |       0.0936 | proposed  |
| RA_noRF                            |     8.05   |        0.948  |       0.1391 | proposed  |
| RA_mean                            |     8.0833 |        0.948  |       0.1392 | proposed  |
| STD_MI                             |     9.6667 |        0.9671 |       0.0933 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=3.042): WITHOUT_FS, SOTA_SHAP_XGB, STD_RFE_RF, RA_noRed, P4_Inter_IntraWeight_Adjustment_FS, F0_Fuzzy_RAR, SOTA_mRMR, STD_ANOVA, RA_Consensus

### Average ranks: RF__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |     4.1667 |        0.9989 |       0.0031 | no_fs     |
| STD_RFE_RF                         |     4.6    |        0.9989 |       0.0031 | classic   |
| SOTA_SHAP_XGB                      |     5      |        0.9887 |       0.0561 | benchmark |
| RA_noRed                           |     5.1667 |        0.9989 |       0.0031 | proposed  |
| P4_Inter_IntraWeight_Adjustment_FS |     5.75   |        0.9783 |       0.0778 | proposed  |
| F0_Fuzzy_RAR                       |     5.9833 |        0.9485 |       0.1393 | proposed  |
| STD_ANOVA                          |     6.6    |        0.968  |       0.0935 | classic   |
| RA_Consensus                       |     7.15   |        0.968  |       0.0935 | proposed  |
| RA_mean                            |     7.5667 |        0.9483 |       0.1393 | proposed  |
| RA_noRF                            |     8.4667 |        0.9481 |       0.1391 | proposed  |
| STD_MI                             |     8.5667 |        0.9483 |       0.1392 | classic   |
| SOTA_mRMR                          |     8.9833 |        0.9091 |       0.1957 | benchmark |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=3.042): WITHOUT_FS, STD_RFE_RF, SOTA_SHAP_XGB, RA_noRed, P4_Inter_IntraWeight_Adjustment_FS, F0_Fuzzy_RAR, STD_ANOVA, RA_Consensus

### Average ranks: XGB__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |     3.4    |        0.9989 |       0.0031 | no_fs     |
| RA_noRed                           |     4.4    |        0.9988 |       0.0031 | proposed  |
| SOTA_SHAP_XGB                      |     4.5333 |        0.9885 |       0.056  | benchmark |
| P4_Inter_IntraWeight_Adjustment_FS |     5.1333 |        0.9781 |       0.0779 | proposed  |
| STD_ANOVA                          |     5.8    |        0.968  |       0.0936 | classic   |
| STD_MI                             |     7.3333 |        0.9484 |       0.1393 | classic   |
| STD_RFE_RF                         |     7.4333 |        0.9984 |       0.0031 | classic   |
| RA_Consensus                       |     7.5333 |        0.9679 |       0.0935 | proposed  |
| RA_mean                            |     7.7167 |        0.9483 |       0.1393 | proposed  |
| F0_Fuzzy_RAR                       |     7.7667 |        0.9687 |       0.121  | proposed  |
| RA_noRF                            |     8.4167 |        0.948  |       0.1392 | proposed  |
| SOTA_mRMR                          |     8.5333 |        0.9091 |       0.1957 | benchmark |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=3.042): WITHOUT_FS, RA_noRed, SOTA_SHAP_XGB, P4_Inter_IntraWeight_Adjustment_FS, STD_ANOVA

## Wilcoxon + Holm: proposed selectors vs the strongest competitors (pooled all-model scope if available)

| ref                                | other                              |   n_blocks |   mean_diff |   p_value |   p_holm | verdict                   |
|:-----------------------------------|:-----------------------------------|-----------:|------------:|----------:|---------:|:--------------------------|
| RA_Consensus                       | P4_Inter_IntraWeight_Adjustment_FS |         90 |    -0.01012 |   0.01121 |  0.04484 | ref worse                 |
| RA_Consensus                       | RA_noRed                           |         90 |    -0.03081 |   0       |  1e-05   | ref worse                 |
| RA_Consensus                       | SOTA_SHAP_XGB                      |         90 |    -0.02406 |   0       |  0       | ref worse                 |
| RA_Consensus                       | STD_RFE_RF                         |         90 |    -0.03077 |   0.00034 |  0.00274 | ref worse                 |
| RA_Consensus                       | WITHOUT_FS                         |         90 |    -0.01136 |   0       |  0       | ref worse                 |
| RA_noRF                            | P4_Inter_IntraWeight_Adjustment_FS |         90 |    -0.03006 |   2e-05   |  0.00017 | ref worse                 |
| RA_noRF                            | RA_Consensus                       |         90 |    -0.01995 |   0.00182 |  0.00909 | ref worse                 |
| RA_noRF                            | RA_noRed                           |         90 |    -0.05076 |   0       |  0       | ref worse                 |
| RA_noRF                            | SOTA_SHAP_XGB                      |         90 |    -0.044   |   0       |  0       | ref worse                 |
| RA_noRF                            | STD_RFE_RF                         |         90 |    -0.05072 |   0       |  1e-05   | ref worse                 |
| RA_noRF                            | WITHOUT_FS                         |         90 |    -0.03131 |   0       |  0       | ref worse                 |
| RA_mean                            | P4_Inter_IntraWeight_Adjustment_FS |         90 |    -0.02987 |   0.00055 |  0.00385 | ref worse                 |
| RA_mean                            | RA_Consensus                       |         90 |    -0.01975 |   0.00881 |  0.05287 | no significant difference |
| RA_mean                            | RA_noRed                           |         90 |    -0.05056 |   0       |  0       | ref worse                 |
| RA_mean                            | SOTA_SHAP_XGB                      |         90 |    -0.04381 |   0       |  0       | ref worse                 |
| RA_mean                            | STD_RFE_RF                         |         90 |    -0.05052 |   1e-05   |  0.0001  | ref worse                 |
| RA_mean                            | WITHOUT_FS                         |         90 |    -0.03111 |   0       |  0       | ref worse                 |
| RA_noRed                           | P4_Inter_IntraWeight_Adjustment_FS |         90 |     0.02069 |   0.01215 |  0.03645 | ref better                |
| RA_noRed                           | RA_Consensus                       |         90 |     0.03081 |   0       |  1e-05   | ref better                |
| RA_noRed                           | SOTA_SHAP_XGB                      |         90 |     0.00675 |   0.82329 |  0.82329 | no significant difference |
| RA_noRed                           | STD_RFE_RF                         |         90 |     4e-05   |   0.03371 |  0.06743 | no significant difference |
| RA_noRed                           | WITHOUT_FS                         |         90 |     0.01945 |   0.00181 |  0.00723 | ref better                |
| F0_Fuzzy_RAR                       | P4_Inter_IntraWeight_Adjustment_FS |         90 |    -0.02567 |   0.09385 |  0.28156 | no significant difference |
| F0_Fuzzy_RAR                       | RA_Consensus                       |         90 |    -0.01555 |   0.55887 |  1       | no significant difference |
| F0_Fuzzy_RAR                       | RA_noRed                           |         90 |    -0.04636 |   0.00024 |  0.00243 | ref worse                 |
| F0_Fuzzy_RAR                       | SOTA_SHAP_XGB                      |         90 |    -0.03961 |   0.00028 |  0.00254 | ref worse                 |
| F0_Fuzzy_RAR                       | STD_RFE_RF                         |         90 |    -0.04632 |   0.04295 |  0.21474 | no significant difference |
| F0_Fuzzy_RAR                       | WITHOUT_FS                         |         90 |    -0.02691 |   0       |  0       | ref worse                 |
| P4_Inter_IntraWeight_Adjustment_FS | RA_Consensus                       |         90 |     0.01012 |   0.01121 |  0.06725 | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | RA_noRed                           |         90 |    -0.02069 |   0.01215 |  0.06725 | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | SOTA_SHAP_XGB                      |         90 |    -0.01394 |   0.04095 |  0.16379 | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | STD_RFE_RF                         |         90 |    -0.02065 |   0.67427 |  0.67427 | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | WITHOUT_FS                         |         90 |    -0.00124 |   0.0014  |  0.00982 | ref worse                 |

Full table: wilcoxon_holm.csv (scope used above: ALL_MODELS__fold_level).

## Win / Tie / Loss (block level, tolerance 0.001)

Summed over every opponent (ALL_MODELS__fold_level):

| ref                                |   win |   tie |   loss |
|:-----------------------------------|------:|------:|-------:|
| F0_Fuzzy_RAR                       |    87 |   807 |     96 |
| P4_Inter_IntraWeight_Adjustment_FS |    89 |   812 |     89 |
| RA_Consensus                       |    61 |   857 |     72 |
| RA_mean                            |    43 |   814 |    133 |
| RA_noRF                            |    38 |   788 |    164 |
| RA_noRed                           |   141 |   832 |     17 |

Significance-level W/T/L across models (per-model Wilcoxon-Holm), by reference vs opponent group:

|                                                     |   sig_win |   sig_tie |   sig_loss |
|:----------------------------------------------------|----------:|----------:|-----------:|
| ('F0_Fuzzy_RAR', 'benchmark')                       |         0 |         5 |          1 |
| ('F0_Fuzzy_RAR', 'classic')                         |         0 |         9 |          0 |
| ('F0_Fuzzy_RAR', 'no_fs')                           |         0 |         2 |          1 |
| ('F0_Fuzzy_RAR', 'proposed')                        |         0 |        14 |          1 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'benchmark') |         1 |         5 |          0 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'classic')   |         1 |         8 |          0 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'no_fs')     |         0 |         3 |          0 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'proposed')  |         1 |        14 |          0 |
| ('RA_Consensus', 'benchmark')                       |         1 |         2 |          3 |
| ('RA_Consensus', 'classic')                         |         1 |         6 |          2 |
| ('RA_Consensus', 'no_fs')                           |         0 |         1 |          2 |
| ('RA_Consensus', 'proposed')                        |         0 |        13 |          2 |
| ('RA_mean', 'benchmark')                            |         0 |         3 |          3 |
| ('RA_mean', 'classic')                              |         0 |         7 |          2 |
| ('RA_mean', 'no_fs')                                |         1 |         0 |          2 |
| ('RA_mean', 'proposed')                             |         0 |        12 |          3 |
| ('RA_noRF', 'benchmark')                            |         0 |         3 |          3 |
| ('RA_noRF', 'classic')                              |         0 |         7 |          2 |
| ('RA_noRF', 'no_fs')                                |         1 |         0 |          2 |
| ('RA_noRF', 'proposed')                             |         0 |        11 |          4 |
| ('RA_noRed', 'benchmark')                           |         2 |         4 |          0 |
| ('RA_noRed', 'classic')                             |         4 |         5 |          0 |
| ('RA_noRed', 'no_fs')                               |         0 |         2 |          1 |
| ('RA_noRed', 'proposed')                            |         9 |         6 |          0 |
