"""
fs_methods.py -- feature-selection methods P1-P4 and the five standard baselines.

These functions are copied VERBATIM from Cell 6 of the supplied Colab notebook
(see 19_colab_full_pipeline.py). Only two additions, neither of which changes
the maths or the defaults:
  * BOOT_ROUNDS / MC_ROUNDS module-level settings (defaults 15 / 30 = original)
    so a smoke test can shrink them from the command line;
  * bootstrap_mi() memoises its result for identical inputs, because P1 and P2
    (and the ablation study) all call it on the same data.
"""
import numpy as np
import pandas as pd
from sklearn.feature_selection import mutual_info_classif, f_classif, chi2
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

SEED = 42
BOOT_ROUNDS = 15
MC_ROUNDS = 30
_MI_CACHE = {}


def clear_cache():
    _MI_CACHE.clear()


def norm01(a):
    a = np.asarray(a, float)
    if np.nanmax(a) - np.nanmin(a) < 1e-12:
        return np.zeros_like(a)
    return np.nan_to_num((a - np.nanmin(a)) / (np.nanmax(a) - np.nanmin(a)))


def corr_abs(X):
    C = X.corr(method="spearman").abs().fillna(0).to_numpy(copy=True)
    np.fill_diagonal(C, 1)
    return C


def bootstrap_mi(X, y, rounds=None, frac=.75):
    rounds = BOOT_ROUNDS if rounds is None else rounds
    key = (id(X), X.shape, id(y), rounds, frac)
    if key in _MI_CACHE:
        return _MI_CACHE[key]
    rng = np.random.default_rng(SEED)
    scores = []
    for r in range(rounds):
        idx = rng.choice(len(X), max(50, int(frac * len(X))), replace=True)
        s = mutual_info_classif(X.iloc[idx], y[idx], random_state=SEED + r)
        scores.append(norm01(s))
    A = np.vstack(scores)
    out = (A.mean(0), 1 - norm01(A.std(0)))
    _MI_CACHE[key] = out
    return out


def P1(X, y, k):
    mi, stab = bootstrap_mi(X, y)
    C = corr_abs(X)
    sel = []; cand = list(range(X.shape[1])); ss = []
    for _ in range(min(k, X.shape[1])):
        best = (-1, None)
        for j in cand:
            D = 1 if not sel else max(1e-8, 1 - np.mean([C[j, s] for s in sel]))
            score = (max(mi[j], 1e-8) ** .50) * (max(stab[j], 1e-8) ** .25) * (D ** .25)
            if score > best[0]:
                best = (score, j)
        ss.append(best[0]); sel.append(best[1]); cand.remove(best[1])
    return sel, ss


def P2(X, y, k):
    mi, stab = bootstrap_mi(X, y)
    C = corr_abs(X)
    order = np.argsort(mi)[::-1]
    red = np.zeros(X.shape[1])
    for pos, j in enumerate(order):
        higher = order[:pos]
        red[j] = np.mean(C[j, higher]) if len(higher) else 0
    best_lam = None; best_u = -1; best_score = None
    for lam in [.1, .25, .5, .75, 1.0]:
        score = mi * (.60 + .40 * stab) / (1 + lam * red)
        top = np.argsort(score)[::-1][:k]
        u = np.mean(score[top]) + .1 * np.mean(stab[top]) - .1 * np.mean(red[top])
        if u > best_u:
            best_u = u; best_lam = lam; best_score = score
    sel = np.argsort(best_score)[::-1][:k].tolist()
    return sel, best_score[sel]


def P3(X, y, k, rounds=None, frac=.70):
    rounds = MC_ROUNDS if rounds is None else rounds
    rng = np.random.default_rng(SEED)
    p = X.shape[1]
    freq = np.zeros(p); mia = np.zeros(p)
    per = max(k, min(p, int(np.ceil(.2 * p))))
    for r in range(rounds):
        idx = rng.choice(len(X), max(50, int(frac * len(X))), replace=False)
        mi = norm01(mutual_info_classif(X.iloc[idx], y[idx], random_state=SEED + r))
        mia += mi
        freq[np.argsort(mi)[::-1][:per]] += 1
    mc = freq / rounds; mi = mia / rounds
    C = corr_abs(X)
    sel = []; cand = list(range(p)); scores = []
    for _ in range(min(k, p)):
        best = (-1, None)
        for j in cand:
            D = 1 if not sel else max(1e-8, 1 - np.mean([C[j, s] for s in sel]))
            s = np.sqrt(max(1e-12, mc[j] * mi[j]) * D)
            if s > best[0]:
                best = (s, j)
        scores.append(best[0]); sel.append(best[1]); cand.remove(best[1])
    return sel, scores


def fisher_scores(X, y):
    A = X.values
    classes, counts = np.unique(y, return_counts=True)
    gm = A.mean(0); inter = np.zeros(A.shape[1]); intra = np.zeros(A.shape[1])
    for c, cnt in zip(classes, counts):
        Ac = A[y == c]; w = cnt / len(y)
        inter += w * (Ac.mean(0) - gm) ** 2
        intra += w * Ac.var(0)
    return norm01(inter / (intra + 1e-12))


def P4(X, y, k):
    A = X.values
    classes, counts = np.unique(y, return_counts=True)
    gm = A.mean(0); inter = np.zeros(A.shape[1]); intra = np.zeros(A.shape[1])
    for c, cnt in zip(classes, counts):
        Ac = A[y == c]; w = cnt / len(y)
        inter += w * (Ac.mean(0) - gm) ** 2
        intra += w * Ac.var(0)
    fisher = norm01(inter / (intra + 1e-12))
    mi = norm01(mutual_info_classif(X, y, random_state=SEED))
    probs = counts / counts.sum()
    ent = -(probs * np.log(probs + 1e-12)).sum() / np.log(len(classes) + 1e-12)
    imbalance = 1 - ent
    eta = float(np.clip(.50 + .25 * imbalance, .50, .75))
    score = eta * fisher + (1 - eta) * mi
    sel = np.argsort(score)[::-1][:k].tolist()
    return sel, score[sel]


def standard_fs(name, X, y, k):
    SEED_ = SEED
    if name == "MI":
        s = mutual_info_classif(X, y, random_state=SEED_)
    elif name == "ANOVA":
        s, _ = f_classif(X, y); s = np.nan_to_num(s)
    elif name == "CHI2":
        Xm = MinMaxScaler().fit_transform(X)
        s, _ = chi2(Xm, y); s = np.nan_to_num(s)
    elif name == "RF_IMPORTANCE":
        m = RandomForestClassifier(n_estimators=250, n_jobs=-1, random_state=SEED_, class_weight="balanced_subsample")
        m.fit(X, y); s = m.feature_importances_
    elif name == "RFE_RF":
        # Baseline used by the reference paper (Yao et al., Computer Networks 271, 2025): Recursive Feature
        # Elimination with a RandomForest base estimator. n_features_to_select=1, step=1 gives a full nested
        # ranking so top-K can be read off for every K in the sweep. Fitted on a subsample for tractability.
        from sklearn.feature_selection import RFE
        rr = np.random.default_rng(SEED_)
        ii = rr.choice(len(X), min(len(X), 15000), replace=False)
        est = RandomForestClassifier(n_estimators=40, max_depth=12, n_jobs=-1, random_state=SEED_,
                                     class_weight="balanced_subsample")
        rfe = RFE(est, n_features_to_select=1, step=1).fit(X.iloc[ii], y[ii])
        s = (X.shape[1] + 1 - rfe.ranking_).astype(float)   # rank 1 (last survivor) -> highest score
    elif name == "L1_LOGISTIC":
        Xs = StandardScaler().fit_transform(X)
        m = LogisticRegression(penalty="l1", solver="saga", C=.5, max_iter=2500, class_weight="balanced", random_state=SEED_)
        m.fit(Xs, y)
        s = np.abs(m.coef_).mean(0)
    sel = np.argsort(s)[::-1][:k].tolist()
    return sel, s[sel]
