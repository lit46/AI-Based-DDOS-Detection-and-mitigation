# Statistical validation (metric: accuracy)

Interpretation notes
- 'Win/Tie/Loss' (your 'wintaylor's') is implemented as Win/Tie/Loss: Win = proposed accuracy higher by more than the tolerance (0.001), Tie = within tolerance, Loss = lower.
- Folds of one CV share training data and repeats reuse the same rows, so blocks are positively correlated; p-values are anti-conservative (Nadeau & Bengio 2003). Use them to rank methods, not as exact error rates.
- With n paired blocks the smallest two-sided Wilcoxon p is 2/2^n; n=5 repeats cannot go below 0.0625, so fold-level blocks (n = repeats x folds) are used.
- Holm correction is applied per (scope, reference method).

## Friedman + Iman-Davenport

| scope                    |   N |   k |     chi2 |   p_friedman |   F_iman_davenport |   df1 |   df2 |   p_iman_davenport |
|:-------------------------|----:|----:|---------:|-------------:|-------------------:|------:|------:|-------------------:|
| KNN__fold_level          |  30 |  12 |  51.6606 |            0 |            5.38248 |    11 |   319 |                  0 |
| RF__fold_level           |  30 |  12 | 152.815  |            0 |           25.0114  |    11 |   319 |                  0 |
| XGB__fold_level          |  30 |  12 | 115.565  |            0 |           15.629   |    11 |   319 |                  0 |
| ALL_MODELS__fold_level   |  90 |  12 | 221.16   |            0 |           25.6013  |    11 |   979 |                  0 |
| ALL_MODELS__repeat_level |   9 |  12 |  61.3734 |            0 |           13.0489  |    11 |    88 |                  0 |

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
| WITHOUT_FS                         |     3.3333 |        0.9999 |       0.0001 | no_fs     |
| SOTA_SHAP_XGB                      |     4.85   |        0.9999 |       0.0001 | benchmark |
| STD_RFE_RF                         |     5.0278 |        0.9999 |       0.0001 | classic   |
| RA_noRed                           |     5.2611 |        0.9999 |       0.0001 | proposed  |
| RA_Consensus                       |     6.6222 |        0.9998 |       0.0001 | proposed  |
| SOTA_mRMR                          |     6.6333 |        0.9998 |       0.0001 | benchmark |
| RA_mean                            |     7.2833 |        0.9998 |       0.0001 | proposed  |
| RA_noRF                            |     7.4222 |        0.9998 |       0.0001 | proposed  |
| P4_Inter_IntraWeight_Adjustment_FS |     7.5889 |        0.9998 |       0.0001 | proposed  |
| STD_MI                             |     7.6444 |        0.9998 |       0.0001 | classic   |
| F0_Fuzzy_RAR                       |     8.0833 |        0.9998 |       0.0002 | proposed  |
| STD_ANOVA                          |     8.25   |        0.9998 |       0.0001 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=1.756): WITHOUT_FS, SOTA_SHAP_XGB, STD_RFE_RF

### Average ranks: ALL_MODELS__repeat_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |     1.1667 |        0.9999 |       0      | no_fs     |
| STD_RFE_RF                         |     3.5556 |        0.9999 |       0.0001 | classic   |
| SOTA_SHAP_XGB                      |     3.9444 |        0.9999 |       0      | benchmark |
| RA_noRed                           |     4.0556 |        0.9999 |       0      | proposed  |
| RA_Consensus                       |     5.8889 |        0.9998 |       0.0001 | proposed  |
| SOTA_mRMR                          |     6.5    |        0.9998 |       0      | benchmark |
| RA_noRF                            |     7.1667 |        0.9998 |       0.0001 | proposed  |
| RA_mean                            |     7.8333 |        0.9998 |       0.0001 | proposed  |
| P4_Inter_IntraWeight_Adjustment_FS |     8.9444 |        0.9998 |       0      | proposed  |
| STD_MI                             |     9.2222 |        0.9998 |       0      | classic   |
| F0_Fuzzy_RAR                       |     9.6667 |        0.9998 |       0.0001 | proposed  |
| STD_ANOVA                          |    10.0556 |        0.9998 |       0.0001 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=5.555): WITHOUT_FS, STD_RFE_RF, SOTA_SHAP_XGB, RA_noRed, RA_Consensus, SOTA_mRMR

### Average ranks: KNN__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |     3.6667 |        0.9999 |       0.0001 | no_fs     |
| RA_Consensus                       |     5.3333 |        0.9999 |       0.0001 | proposed  |
| STD_RFE_RF                         |     5.45   |        0.9999 |       0.0001 | classic   |
| SOTA_mRMR                          |     5.7    |        0.9999 |       0.0001 | benchmark |
| RA_noRF                            |     6.3167 |        0.9999 |       0.0001 | proposed  |
| RA_mean                            |     6.5667 |        0.9998 |       0.0001 | proposed  |
| SOTA_SHAP_XGB                      |     6.7833 |        0.9998 |       0.0001 | benchmark |
| RA_noRed                           |     6.85   |        0.9998 |       0.0001 | proposed  |
| STD_ANOVA                          |     7.2    |        0.9998 |       0.0001 | classic   |
| P4_Inter_IntraWeight_Adjustment_FS |     7.7667 |        0.9998 |       0.0001 | proposed  |
| F0_Fuzzy_RAR                       |     7.9    |        0.9998 |       0.0001 | proposed  |
| STD_MI                             |     8.4667 |        0.9998 |       0.0001 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=3.042): WITHOUT_FS, RA_Consensus, STD_RFE_RF, SOTA_mRMR, RA_noRF, RA_mean

### Average ranks: RF__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |     3.45   |        1      |       0      | no_fs     |
| STD_RFE_RF                         |     3.5167 |        1      |       0      | classic   |
| SOTA_SHAP_XGB                      |     4.0167 |        0.9999 |       0      | benchmark |
| RA_noRed                           |     4.7667 |        0.9999 |       0.0001 | proposed  |
| RA_Consensus                       |     6.5167 |        0.9999 |       0.0001 | proposed  |
| RA_mean                            |     7.2    |        0.9999 |       0.0001 | proposed  |
| F0_Fuzzy_RAR                       |     7.4833 |        0.9999 |       0.0001 | proposed  |
| RA_noRF                            |     7.7833 |        0.9999 |       0.0001 | proposed  |
| SOTA_mRMR                          |     7.7833 |        0.9999 |       0.0001 | benchmark |
| P4_Inter_IntraWeight_Adjustment_FS |     8.05   |        0.9999 |       0.0001 | proposed  |
| STD_MI                             |     8.7167 |        0.9998 |       0.0001 | classic   |
| STD_ANOVA                          |     8.7167 |        0.9999 |       0.0001 | classic   |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=3.042): WITHOUT_FS, STD_RFE_RF, SOTA_SHAP_XGB, RA_noRed

### Average ranks: XGB__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |     2.8833 |        0.9999 |       0.0001 | no_fs     |
| SOTA_SHAP_XGB                      |     3.75   |        0.9999 |       0.0001 | benchmark |
| RA_noRed                           |     4.1667 |        0.9999 |       0.0001 | proposed  |
| STD_MI                             |     5.75   |        0.9998 |       0.0001 | classic   |
| STD_RFE_RF                         |     6.1167 |        0.9998 |       0.0001 | classic   |
| SOTA_mRMR                          |     6.4167 |        0.9998 |       0.0001 | benchmark |
| P4_Inter_IntraWeight_Adjustment_FS |     6.95   |        0.9998 |       0.0001 | proposed  |
| RA_Consensus                       |     8.0167 |        0.9998 |       0.0001 | proposed  |
| RA_mean                            |     8.0833 |        0.9997 |       0.0002 | proposed  |
| RA_noRF                            |     8.1667 |        0.9998 |       0.0002 | proposed  |
| STD_ANOVA                          |     8.8333 |        0.9997 |       0.0001 | classic   |
| F0_Fuzzy_RAR                       |     8.8667 |        0.9996 |       0.0003 | proposed  |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=3.042): WITHOUT_FS, SOTA_SHAP_XGB, RA_noRed, STD_MI

## Wilcoxon + Holm: proposed selectors vs the strongest competitors (pooled all-model scope if available)

| ref                                | other         |   n_blocks |   mean_diff |   p_value |   p_holm | verdict                   |
|:-----------------------------------|:--------------|-----------:|------------:|----------:|---------:|:--------------------------|
| RA_Consensus                       | RA_noRed      |         90 |    -4e-05   |   0.00831 |  0.04153 | ref worse                 |
| RA_Consensus                       | SOTA_SHAP_XGB |         90 |    -5e-05   |   6e-05   |  0.00051 | ref worse                 |
| RA_Consensus                       | SOTA_mRMR     |         90 |    -0       |   0.98232 |  0.98232 | no significant difference |
| RA_Consensus                       | STD_RFE_RF    |         90 |    -4e-05   |   0.00205 |  0.01227 | ref worse                 |
| RA_Consensus                       | WITHOUT_FS    |         90 |    -9e-05   |   0       |  0       | ref worse                 |
| RA_noRF                            | RA_Consensus  |         90 |    -2e-05   |   0.06194 |  0.30972 | no significant difference |
| RA_noRF                            | RA_noRed      |         90 |    -6e-05   |   2e-05   |  0.00014 | ref worse                 |
| RA_noRF                            | SOTA_SHAP_XGB |         90 |    -7e-05   |   0       |  1e-05   | ref worse                 |
| RA_noRF                            | SOTA_mRMR     |         90 |    -2e-05   |   0.0674  |  0.30972 | no significant difference |
| RA_noRF                            | STD_RFE_RF    |         90 |    -5e-05   |   4e-05   |  0.00035 | ref worse                 |
| RA_noRF                            | WITHOUT_FS    |         90 |    -0.0001  |   0       |  0       | ref worse                 |
| RA_mean                            | RA_Consensus  |         90 |    -2e-05   |   0.00099 |  0.00693 | ref worse                 |
| RA_mean                            | RA_noRed      |         90 |    -7e-05   |   4e-05   |  0.00032 | ref worse                 |
| RA_mean                            | SOTA_SHAP_XGB |         90 |    -8e-05   |   0       |  0       | ref worse                 |
| RA_mean                            | SOTA_mRMR     |         90 |    -3e-05   |   0.0277  |  0.13851 | no significant difference |
| RA_mean                            | STD_RFE_RF    |         90 |    -6e-05   |   2e-05   |  0.00015 | ref worse                 |
| RA_mean                            | WITHOUT_FS    |         90 |    -0.00011 |   0       |  0       | ref worse                 |
| RA_noRed                           | RA_Consensus  |         90 |     4e-05   |   0.00831 |  0.02492 | ref better                |
| RA_noRed                           | SOTA_SHAP_XGB |         90 |    -1e-05   |   0.34802 |  0.69604 | no significant difference |
| RA_noRed                           | SOTA_mRMR     |         90 |     4e-05   |   0.00223 |  0.00892 | ref better                |
| RA_noRed                           | STD_RFE_RF    |         90 |     1e-05   |   0.91269 |  0.91269 | no significant difference |
| RA_noRed                           | WITHOUT_FS    |         90 |    -4e-05   |   0       |  1e-05   | ref worse                 |
| F0_Fuzzy_RAR                       | RA_Consensus  |         90 |    -8e-05   |   0.00037 |  0.00223 | ref worse                 |
| F0_Fuzzy_RAR                       | RA_noRed      |         90 |    -0.00013 |   0       |  0       | ref worse                 |
| F0_Fuzzy_RAR                       | SOTA_SHAP_XGB |         90 |    -0.00014 |   0       |  0       | ref worse                 |
| F0_Fuzzy_RAR                       | SOTA_mRMR     |         90 |    -9e-05   |   0.00023 |  0.00159 | ref worse                 |
| F0_Fuzzy_RAR                       | STD_RFE_RF    |         90 |    -0.00012 |   0       |  0       | ref worse                 |
| F0_Fuzzy_RAR                       | WITHOUT_FS    |         90 |    -0.00017 |   0       |  0       | ref worse                 |
| P4_Inter_IntraWeight_Adjustment_FS | RA_Consensus  |         90 |    -2e-05   |   0.08216 |  0.36015 | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | RA_noRed      |         90 |    -6e-05   |   0       |  0       | ref worse                 |
| P4_Inter_IntraWeight_Adjustment_FS | SOTA_SHAP_XGB |         90 |    -7e-05   |   0       |  0       | ref worse                 |
| P4_Inter_IntraWeight_Adjustment_FS | SOTA_mRMR     |         90 |    -2e-05   |   0.02058 |  0.14404 | no significant difference |
| P4_Inter_IntraWeight_Adjustment_FS | STD_RFE_RF    |         90 |    -6e-05   |   2e-05   |  0.0002  | ref worse                 |
| P4_Inter_IntraWeight_Adjustment_FS | WITHOUT_FS    |         90 |    -0.0001  |   0       |  0       | ref worse                 |

Full table: wilcoxon_holm.csv (scope used above: ALL_MODELS__fold_level).

## Win / Tie / Loss (block level, tolerance 0.001)

Summed over every opponent (ALL_MODELS__fold_level):

| ref                                |   win |   tie |   loss |
|:-----------------------------------|------:|------:|-------:|
| F0_Fuzzy_RAR                       |     0 |   979 |     11 |
| P4_Inter_IntraWeight_Adjustment_FS |     1 |   989 |      0 |
| RA_Consensus                       |     1 |   989 |      0 |
| RA_mean                            |     1 |   989 |      0 |
| RA_noRF                            |     1 |   989 |      0 |
| RA_noRed                           |     1 |   989 |      0 |

Significance-level W/T/L across models (per-model Wilcoxon-Holm), by reference vs opponent group:

|                                                     |   sig_win |   sig_tie |   sig_loss |
|:----------------------------------------------------|----------:|----------:|-----------:|
| ('F0_Fuzzy_RAR', 'benchmark')                       |         0 |         3 |          3 |
| ('F0_Fuzzy_RAR', 'classic')                         |         0 |         6 |          3 |
| ('F0_Fuzzy_RAR', 'no_fs')                           |         0 |         0 |          3 |
| ('F0_Fuzzy_RAR', 'proposed')                        |         0 |        12 |          3 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'benchmark') |         0 |         4 |          2 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'classic')   |         1 |         7 |          1 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'no_fs')     |         0 |         0 |          3 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'proposed')  |         1 |        11 |          3 |
| ('RA_Consensus', 'benchmark')                       |         0 |         4 |          2 |
| ('RA_Consensus', 'classic')                         |         4 |         3 |          2 |
| ('RA_Consensus', 'no_fs')                           |         0 |         1 |          2 |
| ('RA_Consensus', 'proposed')                        |         2 |        12 |          1 |
| ('RA_mean', 'benchmark')                            |         0 |         4 |          2 |
| ('RA_mean', 'classic')                              |         1 |         6 |          2 |
| ('RA_mean', 'no_fs')                                |         0 |         1 |          2 |
| ('RA_mean', 'proposed')                             |         0 |        14 |          1 |
| ('RA_noRF', 'benchmark')                            |         0 |         4 |          2 |
| ('RA_noRF', 'classic')                              |         0 |         7 |          2 |
| ('RA_noRF', 'no_fs')                                |         0 |         0 |          3 |
| ('RA_noRF', 'proposed')                             |         0 |        13 |          2 |
| ('RA_noRed', 'benchmark')                           |         2 |         4 |          0 |
| ('RA_noRed', 'classic')                             |         3 |         6 |          0 |
| ('RA_noRed', 'no_fs')                               |         0 |         1 |          2 |
| ('RA_noRed', 'proposed')                            |         7 |         8 |          0 |
