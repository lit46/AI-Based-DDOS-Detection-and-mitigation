# Statistical validation (metric: accuracy)

Interpretation notes
- 'Win/Tie/Loss' (your 'wintaylor's') is implemented as Win/Tie/Loss: Win = proposed accuracy higher by more than the tolerance (0.001), Tie = within tolerance, Loss = lower.
- Folds of one CV share training data and repeats reuse the same rows, so blocks are positively correlated; p-values are anti-conservative (Nadeau & Bengio 2003). Use them to rank methods, not as exact error rates.
- With n paired blocks the smallest two-sided Wilcoxon p is 2/2^n; n=5 repeats cannot go below 0.0625, so fold-level blocks (n = repeats x folds) are used.
- Holm correction is applied per (scope, reference method).

## Friedman + Iman-Davenport

| scope                    |   N |   k |     chi2 |   p_friedman |   F_iman_davenport |   df1 |   df2 |   p_iman_davenport |
|:-------------------------|----:|----:|---------:|-------------:|-------------------:|------:|------:|-------------------:|
| KNN__fold_level          |  50 |  17 |  537.234 |            0 |            100.182 |    16 |   784 |                  0 |
| RF__fold_level           |  50 |  17 |  589.564 |            0 |            137.28  |    16 |   784 |                  0 |
| XGB__fold_level          |  50 |  17 |  583.412 |            0 |            131.988 |    16 |   784 |                  0 |
| ALL_MODELS__fold_level   | 150 |  17 | 1662.37  |            0 |            335.798 |    16 |  2384 |                  0 |
| ALL_MODELS__repeat_level |  15 |  17 |  211.545 |            0 |            104.082 |    16 |   224 |                  0 |

## Nemenyi critical difference

| scope                    |   k |   N |   alpha |   q_alpha_over_sqrt2 |   critical_difference |
|:-------------------------|----:|----:|--------:|---------------------:|----------------------:|
| KNN__fold_level          |  17 |  50 |    0.05 |               3.4584 |                3.4928 |
| RF__fold_level           |  17 |  50 |    0.05 |               3.4584 |                3.4928 |
| XGB__fold_level          |  17 |  50 |    0.05 |               3.4584 |                3.4928 |
| ALL_MODELS__fold_level   |  17 | 150 |    0.05 |               3.4584 |                2.0166 |
| ALL_MODELS__repeat_level |  17 |  15 |    0.05 |               3.4584 |                6.377  |

### Average ranks: ALL_MODELS__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |     2.0667 |        0.9993 |       0.0005 | no_fs     |
| SOTA_SHAP_XGB                      |     2.57   |        0.9992 |       0.0005 | benchmark |
| STD_RFE_RF                         |     3.8233 |        0.9991 |       0.0004 | classic   |
| SOTA_FRFS                          |     5.31   |        0.9835 |       0.0767 | benchmark |
| SOTA_Boruta                        |     6.7367 |        0.993  |       0.0411 | benchmark |
| P4_Inter_IntraWeight_Adjustment_FS |     7.4367 |        0.9854 |       0.0615 | proposed  |
| F0_Fuzzy_RAR                       |     7.5067 |        0.9647 |       0.0967 | proposed  |
| SOTA_ReliefF                       |     8.0433 |        0.9883 |       0.0479 | benchmark |
| SOTA_CMIM                          |     8.4033 |        0.9173 |       0.1353 | benchmark |
| STD_ANOVA                          |     9.2433 |        0.9955 |       0.0015 | classic   |
| STD_CHI2                           |     9.73   |        0.9949 |       0.0019 | classic   |
| SOTA_mRMR                          |    11.28   |        0.9125 |       0.1328 | benchmark |
| P3_MonteCarlo_MI_Fuzzy_FS          |    13.2767 |        0.9093 |       0.1329 | proposed  |
| P1_New_Fuzzy_Rule_FS               |    13.7167 |        0.9095 |       0.1328 | proposed  |
| SOTA_JMIM                          |    14.2867 |        0.949  |       0.0931 | benchmark |
| STD_MI                             |    14.5833 |        0.9242 |       0.1154 | classic   |
| P2_MI_Relevance_Optimization_FS    |    14.9867 |        0.9086 |       0.1321 | proposed  |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=2.017): WITHOUT_FS, SOTA_SHAP_XGB, STD_RFE_RF

### Average ranks: ALL_MODELS__repeat_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |     1.4    |        0.9993 |       0.0005 | no_fs     |
| SOTA_SHAP_XGB                      |     1.6667 |        0.9992 |       0.0003 | benchmark |
| STD_RFE_RF                         |     2.9333 |        0.9991 |       0.0003 | classic   |
| SOTA_Boruta                        |     5.2667 |        0.993  |       0.0125 | benchmark |
| SOTA_FRFS                          |     6.2    |        0.9835 |       0.0211 | benchmark |
| STD_ANOVA                          |     6.6667 |        0.9955 |       0.0003 | classic   |
| P4_Inter_IntraWeight_Adjustment_FS |     7.2667 |        0.9854 |       0.0169 | proposed  |
| SOTA_ReliefF                       |     7.3333 |        0.9883 |       0.0196 | benchmark |
| STD_CHI2                           |     7.6    |        0.9949 |       0.0007 | classic   |
| F0_Fuzzy_RAR                       |     9.7333 |        0.9647 |       0.0251 | proposed  |
| SOTA_JMIM                          |    12.1333 |        0.949  |       0.0415 | benchmark |
| SOTA_CMIM                          |    12.2    |        0.9173 |       0.0024 | benchmark |
| STD_MI                             |    13.5333 |        0.9242 |       0.0225 | classic   |
| SOTA_mRMR                          |    13.5333 |        0.9125 |       0.0031 | benchmark |
| P3_MonteCarlo_MI_Fuzzy_FS          |    15      |        0.9093 |       0.0034 | proposed  |
| P1_New_Fuzzy_Rule_FS               |    15.0667 |        0.9095 |       0.0034 | proposed  |
| P2_MI_Relevance_Optimization_FS    |    15.4667 |        0.9086 |       0.0063 | proposed  |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=6.377): WITHOUT_FS, SOTA_SHAP_XGB, STD_RFE_RF, SOTA_Boruta, SOTA_FRFS, STD_ANOVA, P4_Inter_IntraWeight_Adjustment_FS, SOTA_ReliefF, STD_CHI2

### Average ranks: KNN__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| SOTA_SHAP_XGB                      |       2.83 |        0.9988 |       0.0005 | benchmark |
| WITHOUT_FS                         |       3.46 |        0.9987 |       0.0002 | no_fs     |
| STD_RFE_RF                         |       3.87 |        0.9986 |       0.0004 | classic   |
| SOTA_FRFS                          |       5.33 |        0.98   |       0.0842 | benchmark |
| SOTA_Boruta                        |       6.08 |        0.9973 |       0.0021 | benchmark |
| SOTA_ReliefF                       |       6.19 |        0.995  |       0.0061 | benchmark |
| P4_Inter_IntraWeight_Adjustment_FS |       6.66 |        0.9855 |       0.0619 | proposed  |
| STD_ANOVA                          |       8.54 |        0.9955 |       0.0015 | classic   |
| SOTA_CMIM                          |       8.89 |        0.9168 |       0.1369 | benchmark |
| STD_CHI2                           |       8.96 |        0.9953 |       0.0017 | classic   |
| F0_Fuzzy_RAR                       |       9.42 |        0.9544 |       0.107  | proposed  |
| SOTA_mRMR                          |      12.36 |        0.9088 |       0.1343 | benchmark |
| SOTA_JMIM                          |      13.08 |        0.9767 |       0.0315 | benchmark |
| P3_MonteCarlo_MI_Fuzzy_FS          |      13.74 |        0.9076 |       0.1347 | proposed  |
| P1_New_Fuzzy_Rule_FS               |      13.91 |        0.9083 |       0.1346 | proposed  |
| STD_MI                             |      14.59 |        0.932  |       0.103  | classic   |
| P2_MI_Relevance_Optimization_FS    |      15.09 |        0.9084 |       0.1338 | proposed  |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=3.493): SOTA_SHAP_XGB, WITHOUT_FS, STD_RFE_RF, SOTA_FRFS, SOTA_Boruta, SOTA_ReliefF

### Average ranks: RF__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |       1.58 |        0.9996 |       0.0001 | no_fs     |
| SOTA_SHAP_XGB                      |       2.28 |        0.9995 |       0.0003 | benchmark |
| STD_RFE_RF                         |       3.75 |        0.9993 |       0.0002 | classic   |
| SOTA_FRFS                          |       5.12 |        0.989  |       0.0603 | benchmark |
| F0_Fuzzy_RAR                       |       6.99 |        0.9586 |       0.1089 | proposed  |
| SOTA_Boruta                        |       7.18 |        0.9842 |       0.0707 | benchmark |
| P4_Inter_IntraWeight_Adjustment_FS |       7.79 |        0.9846 |       0.0619 | proposed  |
| SOTA_CMIM                          |       8    |        0.9162 |       0.1359 | benchmark |
| STD_ANOVA                          |       9.05 |        0.9956 |       0.0015 | classic   |
| SOTA_ReliefF                       |       9.14 |        0.9753 |       0.0815 | benchmark |
| STD_CHI2                           |      10.09 |        0.9941 |       0.002  | classic   |
| SOTA_mRMR                          |      10.74 |        0.913  |       0.1328 | benchmark |
| P3_MonteCarlo_MI_Fuzzy_FS          |      12.87 |        0.9064 |       0.1324 | proposed  |
| P1_New_Fuzzy_Rule_FS               |      13.45 |        0.9065 |       0.1324 | proposed  |
| STD_MI                             |      14.48 |        0.9027 |       0.1372 | classic   |
| P2_MI_Relevance_Optimization_FS    |      14.79 |        0.9037 |       0.1313 | proposed  |
| SOTA_JMIM                          |      15.7  |        0.8937 |       0.1403 | benchmark |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=3.493): WITHOUT_FS, SOTA_SHAP_XGB, STD_RFE_RF

### Average ranks: XGB__fold_level

| method                             |   avg_rank |   mean_metric |   std_metric | group     |
|:-----------------------------------|-----------:|--------------:|-------------:|:----------|
| WITHOUT_FS                         |       1.16 |        0.9997 |       0.0001 | no_fs     |
| SOTA_SHAP_XGB                      |       2.6  |        0.9995 |       0.0002 | benchmark |
| STD_RFE_RF                         |       3.85 |        0.9993 |       0.0002 | classic   |
| SOTA_FRFS                          |       5.48 |        0.9816 |       0.0844 | benchmark |
| F0_Fuzzy_RAR                       |       6.11 |        0.9812 |       0.0687 | proposed  |
| SOTA_Boruta                        |       6.95 |        0.9975 |       0.002  | benchmark |
| P4_Inter_IntraWeight_Adjustment_FS |       7.86 |        0.986  |       0.0619 | proposed  |
| SOTA_CMIM                          |       8.32 |        0.919  |       0.136  | benchmark |
| SOTA_ReliefF                       |       8.8  |        0.9946 |       0.0065 | benchmark |
| STD_CHI2                           |      10.14 |        0.9953 |       0.0016 | classic   |
| STD_ANOVA                          |      10.14 |        0.9954 |       0.0016 | classic   |
| SOTA_mRMR                          |      10.74 |        0.9156 |       0.1338 | benchmark |
| P3_MonteCarlo_MI_Fuzzy_FS          |      13.22 |        0.9137 |       0.1341 | proposed  |
| P1_New_Fuzzy_Rule_FS               |      13.79 |        0.9136 |       0.1341 | proposed  |
| SOTA_JMIM                          |      14.08 |        0.9768 |       0.0315 | benchmark |
| STD_MI                             |      14.68 |        0.9378 |       0.1018 | classic   |
| P2_MI_Relevance_Optimization_FS    |      15.08 |        0.9136 |       0.1336 | proposed  |

Methods statistically indistinguishable from the top-ranked one (rank diff <= CD=3.493): WITHOUT_FS, SOTA_SHAP_XGB, STD_RFE_RF

## Wilcoxon + Holm: proposed selectors vs the strongest competitors (pooled all-model scope if available)

| ref                                | other         |   n_blocks |   mean_diff |   p_value |   p_holm | verdict                   |
|:-----------------------------------|:--------------|-----------:|------------:|----------:|---------:|:--------------------------|
| F0_Fuzzy_RAR                       | SOTA_Boruta   |        150 |    -0.0283  |   0.00193 |  0.00963 | ref worse                 |
| F0_Fuzzy_RAR                       | SOTA_SHAP_XGB |        150 |    -0.03455 |   0       |  0       | ref worse                 |
| F0_Fuzzy_RAR                       | STD_ANOVA     |        150 |    -0.03079 |   0.13341 |  0.40023 | no significant difference |
| F0_Fuzzy_RAR                       | STD_CHI2      |        150 |    -0.0302  |   0.06075 |  0.243   | no significant difference |
| F0_Fuzzy_RAR                       | STD_RFE_RF    |        150 |    -0.03437 |   0       |  0       | ref worse                 |
| F0_Fuzzy_RAR                       | WITHOUT_FS    |        150 |    -0.03461 |   0       |  0       | ref worse                 |
| P1_New_Fuzzy_Rule_FS               | SOTA_Boruta   |        150 |    -0.08353 |   0       |  0       | ref worse                 |
| P1_New_Fuzzy_Rule_FS               | SOTA_SHAP_XGB |        150 |    -0.08978 |   0       |  0       | ref worse                 |
| P1_New_Fuzzy_Rule_FS               | STD_ANOVA     |        150 |    -0.08603 |   0       |  0       | ref worse                 |
| P1_New_Fuzzy_Rule_FS               | STD_CHI2      |        150 |    -0.08544 |   0       |  0       | ref worse                 |
| P1_New_Fuzzy_Rule_FS               | STD_RFE_RF    |        150 |    -0.0896  |   0       |  0       | ref worse                 |
| P1_New_Fuzzy_Rule_FS               | WITHOUT_FS    |        150 |    -0.08985 |   0       |  0       | ref worse                 |
| P2_MI_Relevance_Optimization_FS    | SOTA_Boruta   |        150 |    -0.08444 |   0       |  0       | ref worse                 |
| P2_MI_Relevance_Optimization_FS    | SOTA_SHAP_XGB |        150 |    -0.09068 |   0       |  0       | ref worse                 |
| P2_MI_Relevance_Optimization_FS    | STD_ANOVA     |        150 |    -0.08693 |   0       |  0       | ref worse                 |
| P2_MI_Relevance_Optimization_FS    | STD_CHI2      |        150 |    -0.08634 |   0       |  0       | ref worse                 |
| P2_MI_Relevance_Optimization_FS    | STD_RFE_RF    |        150 |    -0.0905  |   0       |  0       | ref worse                 |
| P2_MI_Relevance_Optimization_FS    | WITHOUT_FS    |        150 |    -0.09075 |   0       |  0       | ref worse                 |
| P3_MonteCarlo_MI_Fuzzy_FS          | SOTA_Boruta   |        150 |    -0.08375 |   0       |  0       | ref worse                 |
| P3_MonteCarlo_MI_Fuzzy_FS          | SOTA_SHAP_XGB |        150 |    -0.09    |   0       |  0       | ref worse                 |
| P3_MonteCarlo_MI_Fuzzy_FS          | STD_ANOVA     |        150 |    -0.08624 |   0       |  0       | ref worse                 |
| P3_MonteCarlo_MI_Fuzzy_FS          | STD_CHI2      |        150 |    -0.08565 |   0       |  0       | ref worse                 |
| P3_MonteCarlo_MI_Fuzzy_FS          | STD_RFE_RF    |        150 |    -0.08982 |   0       |  0       | ref worse                 |
| P3_MonteCarlo_MI_Fuzzy_FS          | WITHOUT_FS    |        150 |    -0.09006 |   0       |  0       | ref worse                 |
| P4_Inter_IntraWeight_Adjustment_FS | SOTA_Boruta   |        150 |    -0.00761 |   0       |  0       | ref worse                 |
| P4_Inter_IntraWeight_Adjustment_FS | SOTA_SHAP_XGB |        150 |    -0.01386 |   0       |  0       | ref worse                 |
| P4_Inter_IntraWeight_Adjustment_FS | STD_ANOVA     |        150 |    -0.0101  |   4e-05   |  0.00012 | ref worse                 |
| P4_Inter_IntraWeight_Adjustment_FS | STD_CHI2      |        150 |    -0.00951 |   0       |  0       | ref worse                 |
| P4_Inter_IntraWeight_Adjustment_FS | STD_RFE_RF    |        150 |    -0.01368 |   0       |  0       | ref worse                 |
| P4_Inter_IntraWeight_Adjustment_FS | WITHOUT_FS    |        150 |    -0.01392 |   0       |  0       | ref worse                 |

Full table: wilcoxon_holm.csv (scope used above: ALL_MODELS__fold_level).

## Win / Tie / Loss (block level, tolerance 0.001)

Summed over every opponent (ALL_MODELS__fold_level):

| ref                                |   win |   tie |   loss |
|:-----------------------------------|------:|------:|-------:|
| F0_Fuzzy_RAR                       |  1165 |   582 |    653 |
| P1_New_Fuzzy_Rule_FS               |   312 |   389 |   1699 |
| P2_MI_Relevance_Optimization_FS    |   181 |   296 |   1923 |
| P3_MonteCarlo_MI_Fuzzy_FS          |   343 |   437 |   1620 |
| P4_Inter_IntraWeight_Adjustment_FS |  1175 |   467 |    758 |

Significance-level W/T/L across models (per-model Wilcoxon-Holm), by reference vs opponent group:

|                                                     |   sig_win |   sig_tie |   sig_loss |
|:----------------------------------------------------|----------:|----------:|-----------:|
| ('F0_Fuzzy_RAR', 'benchmark')                       |         6 |         9 |          6 |
| ('F0_Fuzzy_RAR', 'classic')                         |         3 |         4 |          5 |
| ('F0_Fuzzy_RAR', 'no_fs')                           |         0 |         0 |          3 |
| ('F0_Fuzzy_RAR', 'proposed')                        |         9 |         2 |          1 |
| ('P1_New_Fuzzy_Rule_FS', 'benchmark')               |         1 |         2 |         18 |
| ('P1_New_Fuzzy_Rule_FS', 'classic')                 |         1 |         1 |         10 |
| ('P1_New_Fuzzy_Rule_FS', 'no_fs')                   |         0 |         0 |          3 |
| ('P1_New_Fuzzy_Rule_FS', 'proposed')                |         1 |         3 |          8 |
| ('P2_MI_Relevance_Optimization_FS', 'benchmark')    |         1 |         1 |         19 |
| ('P2_MI_Relevance_Optimization_FS', 'classic')      |         0 |         3 |          9 |
| ('P2_MI_Relevance_Optimization_FS', 'no_fs')        |         0 |         0 |          3 |
| ('P2_MI_Relevance_Optimization_FS', 'proposed')     |         3 |         0 |          9 |
| ('P3_MonteCarlo_MI_Fuzzy_FS', 'benchmark')          |         1 |         1 |         19 |
| ('P3_MonteCarlo_MI_Fuzzy_FS', 'classic')            |         1 |         0 |         11 |
| ('P3_MonteCarlo_MI_Fuzzy_FS', 'no_fs')              |         0 |         0 |          3 |
| ('P3_MonteCarlo_MI_Fuzzy_FS', 'proposed')           |         2 |         3 |          7 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'benchmark') |        11 |         4 |          6 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'classic')   |         3 |         1 |          8 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'no_fs')     |         0 |         0 |          3 |
| ('P4_Inter_IntraWeight_Adjustment_FS', 'proposed')  |        10 |         2 |          0 |
