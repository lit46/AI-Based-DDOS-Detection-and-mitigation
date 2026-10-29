"""
selector_rank_consensus.py -- RA_Consensus: fuzzy consensus of three different relevance criteria + a redundancy penalty.

Motivation (from our own results, a hypothesis to be tested, not a finding):
  * MI alone was among the worst on CIC but the best on the UNSW holdout; ANOVA was the reverse; RFE-RF was never far from the best.
  * A feature that ranks well under MI, a class-separation score AND a model-based importance is unlikely to be an artefact of one criterion.

Design (FROZEN before any evaluation; see PROTOCOL_B.md):
  1. Three criteria on the selection subsample: mutual information, ANOVA F, random-forest impurity importance (100 trees, depth 12).
  2. Each criterion -> a fuzzy membership by rank: mu = 1 - (rank-1)/p  (best feature = 1, worst = 1/p).
  3. Consensus = geometric mean of the memberships (a fuzzy AND: one bad criterion pulls the feature down).
  4. Greedy selection: score_j = consensus_j * (1 - max |corr(j, selected)|)   (first pick has no penalty).
Variants for the ablation: RA_noRF (MI + F only), RA_mean (arithmetic mean instead of geometric), RA_noRed (no redundancy penalty).
"""
import numpy as np
from scipy.stats import rankdata
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import f_classif, mutual_info_classif


def _mu(score):
    p = len(score)
    r = rankdata(-np.asarray(score, float), method="average")      # rank 1 = best
    return 1.0 - (r - 1.0) / p


def ra_consensus(X, y, k, seed=42, use_rf=True, agg="geo", use_red=True):
    A = np.nan_to_num(X.values.astype(float)); y = np.asarray(y); p = A.shape[1]
    mems = [_mu(mutual_info_classif(A, y, random_state=seed)), _mu(np.nan_to_num(f_classif(A, y)[0]))]
    if use_rf:
        rf = RandomForestClassifier(n_estimators=100, max_depth=12, n_jobs=1, random_state=seed, class_weight="balanced_subsample").fit(A, y)
        mems.append(_mu(rf.feature_importances_))
    M = np.vstack(mems)
    cons = np.exp(np.log(M).mean(0)) if agg == "geo" else M.mean(0)
    C = np.nan_to_num(np.abs(np.corrcoef(A, rowvar=False)), nan=0.0)
    np.fill_diagonal(C, 0.0)
    sel, rem = [], list(range(p))
    for _ in range(min(k, p)):
        pen = (1 - C[np.ix_(rem, sel)].max(axis=1)) if (sel and use_red) else np.ones(len(rem))
        s = cons[rem] * pen
        j = rem[int(np.argmax(s))]
        sel.append(j); rem.remove(j)
    return sel
