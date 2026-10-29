# Statistical validation (metric: accuracy)

Interpretation notes
- 'Win/Tie/Loss' (your 'wintaylor's') is implemented as Win/Tie/Loss: Win = proposed accuracy higher by more than the tolerance (0.001), Tie = within tolerance, Loss = lower.
- Folds of one CV share training data and repeats reuse the same rows, so blocks are positively correlated; p-values are anti-conservative (Nadeau & Bengio 2003). Use them to rank methods, not as exact error rates.
- With n paired blocks the smallest two-sided Wilcoxon p is 2/2^n; n=5 repeats cannot go below 0.0625, so fold-level blocks (n = repeats x folds) are used.
- Holm correction is applied per (scope, reference method).

## Friedman + Iman-Davenport

| scope                    |   N |   k |     chi2 |   p_friedman |   F_iman_davenport |   df1 |   df2 |   p_iman_davenport |
|:-------------------------|----:|----:|---------:|-------------:|-------------------:|------:|------:|-------------------:|
| KNN__fold_level          |  10 |  12 |  82.9062 |            0 |            27.5397 |    11 |    99 |                  0 |
| RF__fold_level           |  10 |  12 |  82.3385 |            0 |            26.7898 |    11 |    99 |                  0 |
| XGB__fold_level          |  10 |  12 |  79.724  |            0 |            23.6992 |    11 |    99 |                  0 |
| ALL_MODELS__fold_level   |  30 |  12 | 177.855  |            0 |            33.9004 |    11 |   319 |                  0 |
| ALL_MODELS__repeat_level |  30 |  12 | 177.855  |            0 |            33.9004 |    11 |   319 |                  0 |

## Nemenyi critical difference

| scope                    |   k |   N |   alpha |   q_alpha_over_sqrt2 |   critical_difference |
|:-------------------------|----:|----:|--------:|---------------------:|----------------------:|
| KNN__fold_level          |  12 |  10 |    0.05 |                3.268 |                5.2695 |
| RF__fold_level           |  12 |  10 |    0.05 |                3.268 |                5.2695 |
| XGB__fold_level          |  12 |  10 |    0.05 |                3.268 |                5.2695 |
| ALL_MODELS__fold_level   |  12 |  30 |    0.05 |                3.268 |                3.0423 |
| ALL_MODELS__repeat_level |  12 |  30 |    0.05 |                3.268 |                3.0423 |

### Average ranks: ALL_MODELS__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| STD_MI                             |     2.7333 |        0.8688 |       0.0059 | classic   |
| SOTA_mRMR                          |     3.5167 |        0.864  |       0.0082 | benchmark |
| F0_Fuzzy_RAR                       |     4.9333 |        0.8632 |       0.006  | proposed  |
| P4_Inter_IntraWeight_Adjustment_FS |     5.2    |        0.8635 |       0.0058 | proposed  |
| STD_RFE_RF                         |     5.2833 |        0.8609 |       0.0097 | classic   |
| RA_mean                            |     5.6    |        0.8621 |       0.0089 | proposed  |
| RA_Consensus                       |     6.0833 |        0.8607 |       0.0099 | proposed  |
| WITHOUT_FS                         |     6.7667 |        0.857  |       0.014  | no_fs     |
| SOTA_SHAP_XGB                      |     7.6    |        0.8565 |       0.0131 | benchmark |
| RA_noRF                            |     8.05   |        0.8479 |       0.026  | proposed  |
| RA_noRed                           |    10.4    |        0.8433 |       0.0109 | proposed  |
| STD_ANOVA                          |    11.8333 |        0.809  |       0.034  | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=3.042): STD_MI, SOTA_mRMR, F0_Fuzzy_RAR, P4_Inter_IntraWeight_Adjustment_FS, STD_RFE_RF, RA_mean

### Average ranks: ALL_MODELS__repeat_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| STD_MI                             |     2.7333 |        0.8688 |       0.0059 | classic   |
| SOTA_mRMR                          |     3.5167 |        0.864  |       0.0082 | benchmark |
| F0_Fuzzy_RAR                       |     4.9333 |        0.8632 |       0.006  | proposed  |
| P4_Inter_IntraWeight_Adjustment_FS |     5.2    |        0.8635 |       0.0058 | proposed  |
| STD_RFE_RF                         |     5.2833 |        0.8609 |       0.0097 | classic   |
| RA_mean                            |     5.6    |        0.8621 |       0.0089 | proposed  |
| RA_Consensus                       |     6.0833 |        0.8607 |       0.0099 | proposed  |
| WITHOUT_FS                         |     6.7667 |        0.857  |       0.014  | no_fs     |
| SOTA_SHAP_XGB                      |     7.6    |        0.8565 |       0.0131 | benchmark |
| RA_noRF                            |     8.05   |        0.8479 |       0.026  | proposed  |
| RA_noRed                           |    10.4    |        0.8433 |       0.0109 | proposed  |
| STD_ANOVA                          |    11.8333 |        0.809  |       0.034  | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=3.042): STD_MI, SOTA_mRMR, F0_Fuzzy_RAR, P4_Inter_IntraWeight_Adjustment_FS, STD_RFE_RF, RA_mean

### Average ranks: KNN__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| STD_MI                             |       1    |        0.8712 |       0      | classic   |
| F0_Fuzzy_RAR                       |       3.6  |        0.8584 |       0.0028 | proposed  |
| P4_Inter_IntraWeight_Adjustment_FS |       3.8  |        0.8593 |       0.0039 | proposed  |
| RA_mean                            |       5    |        0.8546 |       0.0068 | proposed  |
| RA_Consensus                       |       5.25 |        0.8526 |       0.0109 | proposed  |
| SOTA_mRMR                          |       5.3  |        0.8554 |       0.0017 | benchmark |
| STD_RFE_RF                         |       6.6  |        0.8498 |       0.0046 | classic   |
| RA_noRF                            |       7.35 |        0.8361 |       0.0302 | proposed  |
| SOTA_SHAP_XGB                      |       8.5  |        0.8424 |       0.01   | benchmark |
| RA_noRed                           |       9.6  |        0.8375 |       0.0038 | proposed  |
| WITHOUT_FS                         |      10.1  |        0.8376 |       0      | no_fs     |
| STD_ANOVA                          |      11.9  |        0.7676 |       0.0242 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=5.269): STD_MI, F0_Fuzzy_RAR, P4_Inter_IntraWeight_Adjustment_FS, RA_mean, RA_Consensus, SOTA_mRMR

### Average ranks: RF__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| SOTA_mRMR                          |        1.7 |        0.8746 |       0.0012 | benchmark |
| STD_MI                             |        2.2 |        0.8743 |       0.0003 | classic   |
| RA_mean                            |        4.1 |        0.873  |       0.0015 | proposed  |
| STD_RFE_RF                         |        4.8 |        0.8722 |       0.0012 | classic   |
| RA_Consensus                       |        6   |        0.8706 |       0.0033 | proposed  |
| F0_Fuzzy_RAR                       |        6.1 |        0.8712 |       0.0005 | proposed  |
| P4_Inter_IntraWeight_Adjustment_FS |        6.6 |        0.8707 |       0.0014 | proposed  |
| SOTA_SHAP_XGB                      |        6.6 |        0.8703 |       0.0025 | benchmark |
| RA_noRF                            |        8.1 |        0.8596 |       0.0233 | proposed  |
| WITHOUT_FS                         |        9.2 |        0.8678 |       0.0005 | no_fs     |
| RA_noRed                           |       10.8 |        0.8579 |       0.0012 | proposed  |
| STD_ANOVA                          |       11.8 |        0.8388 |       0.0086 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=5.269): SOTA_mRMR, STD_MI, RA_mean, STD_RFE_RF, RA_Consensus, F0_Fuzzy_RAR, P4_Inter_IntraWeight_Adjustment_FS, SOTA_SHAP_XGB

### Average ranks: XGB__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |       1    |        0.8656 |       0.0007 | no_fs     |
| SOTA_mRMR                          |       3.55 |        0.862  |       0.0016 | benchmark |
| STD_RFE_RF                         |       4.45 |        0.8607 |       0.0013 | classic   |
| STD_MI                             |       5    |        0.8608 |       0.0014 | classic   |
| F0_Fuzzy_RAR                       |       5.1  |        0.8602 |       0.0006 | proposed  |
| P4_Inter_IntraWeight_Adjustment_FS |       5.2  |        0.8604 |       0.0015 | proposed  |
| RA_Consensus                       |       7    |        0.8589 |       0.0017 | proposed  |
| RA_mean                            |       7.7  |        0.8589 |       0.0012 | proposed  |
| SOTA_SHAP_XGB                      |       7.7  |        0.8567 |       0.004  | benchmark |
| RA_noRF                            |       8.7  |        0.8479 |       0.0204 | proposed  |
| RA_noRed                           |      10.8  |        0.8344 |       0.0025 | proposed  |
| STD_ANOVA                          |      11.8  |        0.8205 |       0.0053 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=5.269): WITHOUT_FS, SOTA_mRMR, STD_RFE_RF, STD_MI, F0_Fuzzy_RAR, P4_Inter_IntraWeight_Adjustment_FS

## Wilcoxon + Holm: proposed selectors vs the strongest competitors (pooled all-model scope if available)

| ref                                | other                              |   n_blocks |   mean_diff |   p_value |   p_holm | verdict                   |
|:-----------------------------------|:-----------------------------------|-----------:|------------:|----------:|---------:|:--------------------------|
| RA_Consensus                       | F0_Fuzzy_RAR                       |         30 |    -0.00255 |   0.03872 |  0.19359 | no significant difference |
| RA_Consensus                       | P4_Inter_IntraWeight_Adjustment_FS |         30 |    -0.00277 |   0.20588 |  0.632   | no significant difference |
| RA_Consensus                       | RA_mean                            |         30 |    -0.00143 |   0.158   |  0.632   | no significant difference |
| RA_Consensus                       | SOTA_mRMR                          |         30 |    -0.0033  |   0.01366 |  0.08198 | no significant difference |
| RA_Consensus                       | STD_MI                             |         30 |    -0.00807 |   1e-05   |  8e-05   | ref worse                 |
| RA_Consensus                       | STD_RFE_RF                         |         30 |    -0.00018 |   0.25363 |  0.632   | no significant difference |
| RA_Consensus                       | WITHOUT_FS                         |         30 |     0.00368 |   0.27112 |  0.632   | no significant difference |
| RA_noRF                            | F0_Fuzzy_RAR                       |         30 |    -0.01539 |   0.00011 |  0.00084 | ref worse                 |
| RA_noRF                            | P4_Inter_IntraWeight_Adjustment_FS |         30 |    -0.01561 |   0.00064 |  0.00447 | ref worse                 |
| RA_noRF                            | RA_mean                            |         30 |    -0.01427 |   0.00096 |  0.00523 | ref worse                 |
| RA_noRF                            | SOTA_mRMR                          |         30 |    -0.01614 |   2e-05   |  0.00016 | ref worse                 |
| RA_noRF                            | STD_MI                             |         30 |    -0.02091 |   1e-05   |  6e-05   | ref worse                 |
| RA_noRF                            | STD_RFE_RF                         |         30 |    -0.01302 |   0.00087 |  0.00523 | ref worse                 |
| RA_noRF                            | WITHOUT_FS                         |         30 |    -0.00916 |   0.25359 |  0.50719 | no significant difference |
| RA_mean                            | F0_Fuzzy_RAR                       |         30 |    -0.00112 |   0.47789 |  1       | no significant difference |
| RA_mean                            | P4_Inter_IntraWeight_Adjustment_FS |         30 |    -0.00134 |   0.5786  |  1       | no significant difference |
| RA_mean                            | SOTA_mRMR                          |         30 |    -0.00187 |   0.00821 |  0.04928 | ref worse                 |
| RA_mean                            | STD_MI                             |         30 |    -0.00664 |   1e-05   |  6e-05   | ref worse                 |
| RA_mean                            | STD_RFE_RF                         |         30 |     0.00125 |   0.829   |  1       | no significant difference |
| RA_mean                            | WITHOUT_FS                         |         30 |     0.00512 |   0.04266 |  0.21328 | no significant difference |
| RA_noRed                           | F0_Fuzzy_RAR                       |         30 |    -0.01997 |   0       |  2e-05   | ref worse                 |
| RA_noRed                           | P4_Inter_IntraWeight_Adjustment_FS |         30 |    -0.02018 |   0       |  2e-05   | ref worse                 |
| RA_noRed                           | RA_mean                            |         30 |    -0.01885 |   0       |  2e-05   | ref worse                 |
| RA_noRed                           | SOTA_mRMR                          |         30 |    -0.02072 |   0       |  2e-05   | ref worse                 |
| RA_noRed                           | STD_MI                             |         30 |    -0.02549 |   0       |  2e-05   | ref worse                 |
| RA_noRed                           | STD_RFE_RF                         |         30 |    -0.01759 |   0       |  2e-05   | ref worse                 |
| RA_noRed                           | WITHOUT_FS                         |         30 |    -0.01373 |   3e-05   |  6e-05   | ref worse                 |
| F0_Fuzzy_RAR                       | P4_Inter_IntraWeight_Adjustment_FS |         30 |    -0.00022 |   0.82095 |  0.95578 | no significant difference |
| F0_Fuzzy_RAR                       | RA_mean                            |         30 |     0.00112 |   0.47789 |  0.95578 | no significant difference |
| F0_Fuzzy_RAR                       | SOTA_mRMR                          |         30 |    -0.00076 |   0.07672 |  0.38361 | no significant difference |
| F0_Fuzzy_RAR                       | STD_MI                             |         30 |    -0.00552 |   1e-05   |  8e-05   | ref worse                 |
| F0_Fuzzy_RAR                       | STD_RFE_RF                         |         30 |     0.00237 |   0.14414 |  0.43242 | no significant difference |
| F0_Fuzzy_RAR                       | WITHOUT_FS                         |         30 |     0.00623 |   0.10168 |  0.4067  | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | F0_Fuzzy_RAR                       |         30 |     0.00022 |   0.82095 |  1       | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | RA_mean                            |         30 |     0.00134 |   0.5786  |  1       | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | SOTA_mRMR                          |         30 |    -0.00054 |   0.38201 |  1       | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | STD_MI                             |         30 |    -0.0053  |   3e-05   |  0.00023 | ref worse                 |
| P4_Inter_IntraWeight_Adjustment_FS | STD_RFE_RF                         |         30 |     0.00259 |   0.1499  |  0.74948 | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | WITHOUT_FS                         |         30 |     0.00645 |   0.04916 |  0.29497 | no significant difference |

Full table: wilcoxon_holm.csv (scope used above: ALL_MODELS__fold_level).

## Win / Tie / Loss (block level, tolerance 0.001)

Summed over every opponent (ALL_MODELS__fold_level):

| ref                                |   win |   tie |   loss |
|:-----------------------------------|------:|------:|-------:|
| F0_Fuzzy_RAR                       |   181 |    53 |     96 |
| P4_Inter_IntraWeight_Adjustment_FS |   181 |    50 |     99 |
| RA_Consensus                       |   149 |    57 |    124 |
| RA_mean                            |   173 |    46 |    111 |
| RA_noRF                            |   103 |    36 |    191 |
| RA_noRed                           |    45 |     4 |    281 |

Significance-level W/T/L across models (per-model Wilcoxon-Holm), by reference vs opponent group:

|                                                     |   sig_win |   sig_tie |   sig_loss |
|:----------------------------------------------------|----------:|----------:|-----------:|
| ('F0_Fuzzy_RAR', 'benchmark')                       |         1 |         4 |          1 |
| ('F0_Fuzzy_RAR', 'classic')                         |         4 |         3 |          2 |
| ('F0_Fuzzy_RAR', 'no_fs')                           |         2 |         0 |          1 |
| ('F0_Fuzzy_RAR', 'proposed')                        |         4 |        10 |          1 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'benchmark') |         1 |         4 |          1 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'classic')   |         4 |         3 |          2 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'no_fs')     |         2 |         0 |          1 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'proposed')  |         3 |        12 |          0 |
| ('RA_Consensus', 'benchmark')                       |         0 |         4 |          2 |
| ('RA_Consensus', 'classic')                         |         3 |         4 |          2 |
| ('RA_Consensus', 'no_fs')                           |         1 |         1 |          1 |
| ('RA_Consensus', 'proposed')                        |         3 |        12 |          0 |
| ('RA_mean', 'benchmark')                            |         0 |         4 |          2 |
| ('RA_mean', 'classic')                              |         3 |         5 |          1 |
| ('RA_mean', 'no_fs')                                |         2 |         0 |          1 |
| ('RA_mean', 'proposed')                             |         4 |        11 |          0 |
| ('RA_noRF', 'benchmark')                            |         0 |         5 |          1 |
| ('RA_noRF', 'classic')                              |         1 |         5 |          3 |
| ('RA_noRF', 'no_fs')                                |         0 |         2 |          1 |
| ('RA_noRF', 'proposed')                             |         0 |        14 |          1 |
| ('RA_noRed', 'benchmark')                           |         0 |         1 |          5 |
| ('RA_noRed', 'classic')                             |         3 |         0 |          6 |
| ('RA_noRed', 'no_fs')                               |         0 |         1 |          2 |
| ('RA_noRed', 'proposed')                            |         0 |         3 |         12 |
