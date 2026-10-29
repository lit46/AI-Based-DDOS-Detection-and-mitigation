"""
selectors_all.py -- every feature selector used in the CV study, behind ONE interface:

        ranking = SELECTORS[name](X: DataFrame, y: int ndarray, k: int, seed: int) -> list[int]   # top-k column positions, best first

Groups
------
PROPOSED  F0_Fuzzy_RAR                      script 10 (relevance / association / redundancy, product t-norm), verbatim logic
          P1..P4                            Colab Cell 6 (fs_methods.py), unchanged
CLASSIC   STD_MI, STD_ANOVA, STD_CHI2, STD_RF_IMPORTANCE, STD_L1_LOGISTIC     textbook filters / embedded
          STD_RFE_RF                        Recursive Feature Elimination + RandomForest  (the reference paper's selector)
BENCHMARK SOTA_mRMR      Peng, Long & Ding, IEEE TPAMI 27(8):1226-1238, 2005           (MID form: MI relevance - mean |Spearman| redundancy)
          SOTA_ReliefF   Kononenko, ECML 1994                                         (10 neighbours, subsampled)
          SOTA_CMIM      Fleuret, JMLR 5:1531-1555, 2004                              (equal-frequency discretisation, 10 bins)
          SOTA_JMIM      Bennasar, Hicks & Setchi, Expert Syst. Appl. 42(22):8520-8532, 2015   (same discretisation)
          SOTA_Boruta    Kursa & Rudnicki, J. Stat. Softw. 36(11):1-13, 2010          (SIMPLIFIED: shadow-feature hit counts, no statistical test)
          SOTA_SHAP_XGB  Lundberg & Lee, NeurIPS 2017 / Lundberg et al., Nat. Mach. Intell. 2020   (mean |TreeSHAP| of an XGBoost model)
          SOTA_FRFS      Jensen & Shen, Fuzzy Sets and Systems 141(3):469-485, 2004   (fuzzy-rough QuickReduct on a stratified subsample)

Honest labelling: Boruta is a simplified re-implementation; mRMR is the MID variant with a correlation redundancy
term; CMIM/JMIM/FRFS use my own discretisation/scaling choices. They follow the published criteria, not the authors' code.
"""
import time
import numpy as np
import pandas as pd
from scipy.stats import rankdata
from sklearn.feature_selection import mutual_info_classif
from sklearn.ensemble import RandomForestClassifier

import fs_methods as fsm


# ---------------------------------------------------------------------------------------------- helpers
def strat_idx(y, n, rng, min_per_class=50):
    """Stratified row subsample of size ~n with at least min_per_class rows per class (when available)."""
    if n >= len(y):
        return np.arange(len(y))
    out = []
    for c in np.unique(y):
        ic = np.where(y == c)[0]
        m = min(len(ic), max(min_per_class, int(round(n * len(ic) / len(y)))))
        out.append(rng.choice(ic, m, replace=False))
    return np.sort(np.concatenate(out))


def minmax_normalize(arr):
    arr = np.asarray(arr, dtype=float)
    lo, hi = arr.min(), arr.max()
    if hi - lo < 1e-12:
        return np.zeros_like(arr)
    return (arr - lo) / (hi - lo)


# ---------------------------------------------------------------------------------------------- F0 (script 10)
def f0_fuzzy_rar(X, y, k, seed=42, use_rel=True, use_assoc=True, use_red=True, agg="product"):
    """Script 10's fuzzy rule: score = rel_mem * (1-assoc_mem) * (1-red_mem(S)), greedy. Flags exist for the ablation."""
    A = X.values.astype(float)
    p = A.shape[1]
    rel = minmax_normalize(mutual_info_classif(A, y, discrete_features=False, random_state=seed))
    C = np.nan_to_num(np.corrcoef(A, rowvar=False), nan=0.0)
    np.fill_diagonal(C, 0.0)
    assoc = minmax_normalize(np.abs(C).mean(axis=1))
    sel, rem = [], list(range(p))
    for _ in range(min(k, p)):
        red = minmax_normalize(np.array([np.abs(C[i, sel]).mean() for i in rem]) if sel else np.zeros(len(rem)))
        r = rel[rem] if use_rel else np.ones(len(rem))
        a = (1 - assoc[rem]) if use_assoc else np.ones(len(rem))
        d = (1 - red) if use_red else np.ones(len(rem))
        if agg == "product":
            s = r * a * d
        else:  # additive aggregation (ablation)
            n_on = max(1, int(use_rel) + int(use_assoc) + int(use_red))
            s = (r * use_rel + a * use_assoc + d * use_red) / n_on
        j = rem[int(np.argmax(s))]
        sel.append(j); rem.remove(j)
    return sel


# ---------------------------------------------------------------------------------------------- mRMR
def mrmr(X, y, k, seed=42):
    A = X.values.astype(float)
    rel = mutual_info_classif(A, y, random_state=seed)
    C = fsm.corr_abs(X)
    sel = [int(np.argmax(rel))]
    red_sum = C[:, sel[0]].copy()
    while len(sel) < min(k, A.shape[1]):
        score = rel - red_sum / len(sel)
        score[sel] = -np.inf
        j = int(np.argmax(score))
        sel.append(j); red_sum += C[:, j]
    return sel


# ---------------------------------------------------------------------------------------------- ReliefF
def relieff(X, y, k, seed=42, n_inst=400, n_ref=1500, kn=10):
    rng = np.random.default_rng(seed)
    idx = strat_idx(y, n_ref, rng, 30)
    A = X.values[idx].astype(float); yy = y[idx]; n, p = A.shape
    R = np.empty_like(A)
    for j in range(p):                      # rank-uniform scaling to [0,1] (robust to heavy tails)
        R[:, j] = (rankdata(A[:, j], method="average") - 1) / max(n - 1, 1)
    tg = rng.choice(n, min(n_inst, n), replace=False)
    D = np.zeros((len(tg), n))
    for j in range(p):
        D += np.abs(R[tg, j][:, None] - R[:, j][None, :])
    D[np.arange(len(tg)), tg] = np.inf      # exclude self
    classes, counts = np.unique(yy, return_counts=True)
    prior = dict(zip(classes, counts / n))
    W = np.zeros(p)
    for t, i in enumerate(tg):
        same = np.where((yy == yy[i]) & (np.arange(n) != i))[0]
        if len(same):
            h = same[np.argsort(D[t, same])[:kn]]
            W -= np.abs(R[i] - R[h]).mean(0) / len(tg)
        for c in classes:
            if c == yy[i]:
                continue
            oc = np.where(yy == c)[0]
            m = oc[np.argsort(D[t, oc])[:kn]]
            W += (prior[c] / (1 - prior[yy[i]])) * np.abs(R[i] - R[m]).mean(0) / len(tg)
    return list(np.argsort(W)[::-1][:k])


# ---------------------------------------------------------------------------------------------- CMIM / JMIM (discretised)
def _disc(A, bins=10):
    D = np.zeros(A.shape, dtype=np.int64)
    for j in range(A.shape[1]):
        edges = np.unique(np.quantile(A[:, j], np.linspace(0, 1, bins + 1)[1:-1]))
        D[:, j] = np.searchsorted(edges, A[:, j], side="right")
    return D


def _H(code):
    c = np.bincount(code)
    c = c[c > 0] / len(code)
    return float(-(c * np.log(c)).sum())


def _joint(a, b):
    return a * (int(b.max()) + 1) + b


def _mi(a, b):
    return _H(a) + _H(b) - _H(_joint(a, b))


def _cmi(a, b, c):  # I(a; b | c)
    ac, bc, abc = _joint(a, c), _joint(b, c), _joint(_joint(a, b), c)
    return _H(ac) + _H(bc) - _H(c) - _H(abc)


def cmim(X, y, k, seed=42):
    D = _disc(X.values.astype(float)); p = D.shape[1]
    y = np.asarray(y, dtype=np.int64)
    score = np.array([_mi(D[:, j], y) for j in range(p)])
    sel = [int(np.argmax(score))]
    while len(sel) < min(k, p):
        s = sel[-1]
        for j in range(p):
            if j not in sel:
                score[j] = min(score[j], _cmi(D[:, j], y, D[:, s]))
        cand = [j for j in range(p) if j not in sel]
        sel.append(cand[int(np.argmax(score[cand]))])
    return sel


def jmim(X, y, k, seed=42):
    D = _disc(X.values.astype(float)); p = D.shape[1]
    y = np.asarray(y, dtype=np.int64)
    score = np.array([_mi(D[:, j], y) for j in range(p)])
    sel = [int(np.argmax(score))]
    while len(sel) < min(k, p):
        s = sel[-1]
        for j in range(p):
            if j not in sel:
                score[j] = min(score[j], _mi(_joint(D[:, j], D[:, s]), y))
        cand = [j for j in range(p) if j not in sel]
        sel.append(cand[int(np.argmax(score[cand]))])
    return sel


# ---------------------------------------------------------------------------------------------- Boruta-style
def boruta_style(X, y, k, seed=42, n_iter=12, n_sub=5000):
    rng = np.random.default_rng(seed)
    idx = strat_idx(y, n_sub, rng, 50)
    A = X.values[idx].astype(float); yy = y[idx]; p = A.shape[1]
    hits = np.zeros(p); imp_sum = np.zeros(p)
    for it in range(n_iter):
        sh = A.copy()
        for j in range(p):
            sh[:, j] = rng.permutation(sh[:, j])
        rf = RandomForestClassifier(n_estimators=60, max_depth=10, n_jobs=1, random_state=seed + it,
                                    class_weight="balanced_subsample").fit(np.hstack([A, sh]), yy)
        imp = rf.feature_importances_
        hits += imp[:p] > imp[p:].max()
        imp_sum += imp[:p]
    order = np.lexsort((-imp_sum, -hits))   # primary: hits, secondary: mean importance
    return [int(i) for i in order[:k]]


# ---------------------------------------------------------------------------------------------- SHAP (XGBoost TreeSHAP)
def shap_xgb(X, y, k, seed=42, n_sub=4000):
    import xgboost as xgb
    rng = np.random.default_rng(seed)
    idx = strat_idx(y, n_sub, rng, 50)
    A = X.values[idx].astype(float); yy = y[idx]
    classes = np.unique(yy)
    remap = {c: i for i, c in enumerate(classes)}
    yy = np.array([remap[c] for c in yy])
    clf = xgb.XGBClassifier(n_estimators=80, max_depth=4, learning_rate=0.1, subsample=0.8, n_jobs=1,
                            random_state=seed, objective="multi:softprob" if len(classes) > 2 else "binary:logistic")
    clf.fit(A, yy)
    contrib = clf.get_booster().predict(xgb.DMatrix(A), pred_contribs=True)
    imp = np.abs(contrib[..., :-1]).reshape(-1, A.shape[1]).mean(0)
    return list(np.argsort(imp)[::-1][:k])


# ---------------------------------------------------------------------------------------------- FRFS (fuzzy-rough QuickReduct)
def frfs(X, y, k, seed=42, n_sub=800):
    """Jensen & Shen fuzzy-rough QuickReduct with crisp decision classes.
    Per-feature fuzzy similarity  s_f(x,z) = 1 - |r_f(x) - r_f(z)|  (r = rank-uniform scaling to [0,1]);
    subset similarity = min over features (min t-norm);  positive-region membership of x = 1 - max_{z: class(z)!=class(x)} s_B(x,z);
    dependency gamma(B) = mean_x membership.  Greedy forward: add the feature with the largest gamma until k chosen.
    When gamma stops increasing, the remaining slots are filled by mutual-information rank (documented fallback)."""
    rng = np.random.default_rng(seed)
    idx = strat_idx(y, n_sub, rng, 30)
    A = X.values[idx].astype(float); yy = y[idx]; n, p = A.shape
    R = np.empty((n, p), dtype=np.float32)
    for j in range(p):
        R[:, j] = (rankdata(A[:, j], method="average") - 1) / max(n - 1, 1)
    other = yy[:, None] != yy[None, :]
    cur = np.ones((n, n), dtype=np.float32)
    sel, rem, dep_prev = [], list(range(p)), 0.0
    for _ in range(min(k, p)):
        best = (-1.0, None, None)
        for f in rem:
            s = np.minimum(cur, 1 - np.abs(R[:, f][:, None] - R[:, f][None, :]))
            dep = float((1 - np.where(other, s, 0).max(axis=1)).mean())
            if dep > best[0] + 1e-12:
                best = (dep, f, s)
        if best[0] <= dep_prev + 1e-9 and sel:
            mi = mutual_info_classif(A[:, rem], yy, random_state=seed)
            fill = [rem[i] for i in np.argsort(mi)[::-1][: min(k, p) - len(sel)]]
            return sel + fill
        sel.append(best[1]); rem.remove(best[1]); cur = best[2]; dep_prev = best[0]
    return sel


# ---------------------------------------------------------------------------------------------- registry
def _p(fn):
    return lambda X, y, k, seed: list(fn(X, y, k)[0])


def _std(name):
    return lambda X, y, k, seed: list(fsm.standard_fs(name, X, y, k)[0])


SELECTORS = {
    "F0_Fuzzy_RAR": lambda X, y, k, seed: f0_fuzzy_rar(X, y, k, seed),
    "P1_New_Fuzzy_Rule_FS": _p(fsm.P1),
    "P2_MI_Relevance_Optimization_FS": _p(fsm.P2),
    "P3_MonteCarlo_MI_Fuzzy_FS": _p(fsm.P3),
    "P4_Inter_IntraWeight_Adjustment_FS": _p(fsm.P4),
    "STD_MI": _std("MI"), "STD_ANOVA": _std("ANOVA"), "STD_CHI2": _std("CHI2"),
    "STD_RF_IMPORTANCE": _std("RF_IMPORTANCE"), "STD_L1_LOGISTIC": _std("L1_LOGISTIC"), "STD_RFE_RF": _std("RFE_RF"),
    "SOTA_mRMR": mrmr, "SOTA_ReliefF": relieff, "SOTA_CMIM": cmim, "SOTA_JMIM": jmim,
    "SOTA_Boruta": boruta_style, "SOTA_SHAP_XGB": shap_xgb, "SOTA_FRFS": frfs,
}
from selector_cluster_robust import cr_fuzzy                    # noqa: E402  (new, unvalidated; see its docstring)
SELECTORS.update({
    "CR_Fuzzy_RAR": lambda X, y, k, seed: cr_fuzzy(X, y, k, seed),
    "CR_noSpread": lambda X, y, k, seed: cr_fuzzy(X, y, k, seed, lam=0.0),
    "CR_randomFolds": lambda X, y, k, seed: cr_fuzzy(X, y, k, seed, cluster_folds=False),
    "CR_noAssoc": lambda X, y, k, seed: cr_fuzzy(X, y, k, seed, use_assoc=False),
    "CR_noRed": lambda X, y, k, seed: cr_fuzzy(X, y, k, seed, use_red=False),
})
from selector_rank_consensus import ra_consensus                # noqa: E402  (new, unvalidated; frozen design, see PROTOCOL_B.md)
SELECTORS.update({
    "RA_Consensus": lambda X, y, k, seed: ra_consensus(X, y, k, seed),
    "RA_noRF": lambda X, y, k, seed: ra_consensus(X, y, k, seed, use_rf=False),
    "RA_mean": lambda X, y, k, seed: ra_consensus(X, y, k, seed, agg="mean"),
    "RA_noRed": lambda X, y, k, seed: ra_consensus(X, y, k, seed, use_red=False),
})
from selector_hasan import hasan_top5_published, hasan_xgb_gain  # noqa: E402  (claim test of Hasan et al. 2025, see PROTOCOL_C.md)
SELECTORS.update({
    "HASAN_Top5_Published": lambda X, y, k, seed: hasan_top5_published(X, y, k, seed),
    "HASAN_XGB_Gain5": lambda X, y, k, seed: hasan_xgb_gain(X, y, k, seed),
})
GROUP = {n: ("proposed" if n.startswith(("F0", "P", "CR_", "RA_")) else "classic" if n.startswith("STD_") else "benchmark") for n in SELECTORS}
PROPOSED = [n for n in SELECTORS if GROUP[n] == "proposed"]


def rank_one(name, X, y, k, seed, boot_rounds, mc_rounds):
    """Worker used by joblib: returns (name, ranked column list, seconds)."""
    fsm.SEED = seed
    fsm.BOOT_ROUNDS, fsm.MC_ROUNDS = boot_rounds, mc_rounds
    fsm.clear_cache()                       # the MI cache is keyed on id(X): never trust it across tasks
    t0 = time.time()
    r = SELECTORS[name](X, y, k, seed)
    return name, [int(i) for i in r][:k], time.time() - t0
