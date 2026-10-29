# Protocol C: testing the claim of Hasan, Eaman & Hassan (2025) (written before any real-data run)

**Claim under test** (Procedia Computer Science 265, 124-131): on CIC-DDoS2019 attack-type classification, five features
(ACK Flag Count, Bwd Packets/s, URG Flag Count, Fwd Packet Length Min, Init Fwd Win Bytes) lose "less than 1%" accuracy
relative to the full feature set, for XGBoost and an MLP.

## Setup (fixed now)
- Data: our prepared CIC-DDoS2019 file, restricted to Normal, Syn, UDP, MSSQL, LDAP (their five classes) by `hasan_prepare.py`.
- Features: Inbound and ports always removed (`--drop_ports`); "all features" = everything left after our cleaning (constant columns removed).
- Models: RF and XGBoost (the paper's MLP is NOT reproduced).
- Competitors at the same K=5: RFE-RF, MI, ANOVA, mRMR, SHAP-XGB, plus their *procedure* (XGBoost gain, 100 trees, depth 3, lr 0.1) re-run on each training fold.
- Protocols: (a) duplicate-grouped 10-fold CV x3, (b) the same after exact de-duplication, (c) plain stratified 10-fold x3 (their style),
  (d) day 1 -> day 2 hold-out x5 seeds (their validation style, if the prepared file has both days).

## Decision rule
The claim is **supported under a protocol** if, for BOTH RF and XGBoost, the mean paired accuracy gap (all features minus published top-5) is <= 1.0 point.
It is **not supported** otherwise. Reported either way, together with: bootstrap 95% CI of the gap over folds (optimistic: folds are correlated),
macro-F1 gap, per-class recall of each class, and whether their procedure selects their features on our data.

## Known deviations (stated up front)
1. Not their exact rows: our file is capped/de-duplicated by the adapter; their sample is ~115k rows read off their Fig. 2.
2. Their ranking model sees the whole training set; here it sees the stratified selection subsample (`--fs_rows`, default 5000) of each training fold.
3. Baseline "all features" excludes ports and Inbound; the paper does not say whether it kept ports.
4. No MLP.
5. A different result does not show their numbers are wrong on their data; it shows what the claim is worth under a stricter protocol.
