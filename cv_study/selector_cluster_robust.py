"""
selector_cluster_robust.py -- CR_Fuzzy_RAR: a cluster-robust version of the F0 fuzzy relevance x (1-association) x (1-redundancy) rule.

Why: in the CIC grouped-CV diagnostic, MI-based selectors chose the same packet-size features in good and bad folds and
missed whole attack types (UDPLag, Syn) when those were held out. MI on the pooled training rows cannot see that.

Idea (a design hypothesis, NOT yet validated):
  1. Cluster the training rows in rank-scaled feature space (KMeans). A cluster is a 'kind of traffic'.
  2. Inner folds hold out WHOLE clusters. For each feature, a depth-3 stump trained on the other clusters is scored on the
     held-out cluster (balanced accuracy). That measures whether the feature still separates classes on traffic it has not seen.
  3. relevance = mean over inner folds - lam * std over inner folds   (features that only work in some clusters are penalised).
  4. Same fuzzy aggregation and greedy loop as F0: relevance * (1 - association) * (1 - redundancy(selected)).
Variants (for the ablation) are registered in selectors_all.py:  CR_Fuzzy_RAR, CR_noSpread, CR_randomFolds, CR_noAssoc, CR_noRed.
"""
import numpy as np
from scipy.stats import rankdata
from sklearn.cluster import KMeans
from sklearn.metrics import balanced_accuracy_score
from sklearn.tree import DecisionTreeClassifier


def _mm(a):
    a = np.asarray(a, float); lo, hi = a.min(), a.max()
    return np.zeros_like(a) if hi - lo < 1e-12 else (a - lo) / (hi - lo)


def cr_relevance(A, y, seed=42, n_clusters=8, n_inner=5, lam=1.0, cluster_folds=True, depth=3):
    n, p = A.shape
    R = np.empty_like(A)
    for j in range(p):
        R[:, j] = (rankdata(A[:, j], method="average") - 1) / max(n - 1, 1)
    rng = np.random.default_rng(seed)
    if cluster_folds:
        ncl = int(max(2, min(n_clusters, n // 100)))
        g = KMeans(n_clusters=ncl, n_init=3, random_state=seed).fit_predict(R)
    else:                                              # ablation: random folds instead of cluster folds
        g = rng.integers(0, n_inner, n)
    ug = np.unique(g)
    if len(ug) > n_inner:                              # merge clusters into n_inner groups of clusters
        order = rng.permutation(ug)
        fold_of = {c: i % n_inner for i, c in enumerate(order)}
        g = np.array([fold_of[c] for c in g]); ug = np.unique(g)
    sc = []
    for f in ug:
        te, tr = np.where(g == f)[0], np.where(g != f)[0]
        if len(te) < 20 or len(np.unique(y[tr])) < 2:
            continue
        row = np.zeros(p)
        for j in range(p):
            t = DecisionTreeClassifier(max_depth=depth, class_weight="balanced", random_state=seed)
            t.fit(A[tr, j:j + 1], y[tr])
            row[j] = balanced_accuracy_score(y[te], t.predict(A[te, j:j + 1]))
        sc.append(row)
    if not sc:                                         # degenerate: fall back to a single stump score on all rows
        sc = [np.array([balanced_accuracy_score(y, DecisionTreeClassifier(max_depth=depth, class_weight="balanced", random_state=seed)
                        .fit(A[:, j:j + 1], y).predict(A[:, j:j + 1])) for j in range(p)])]
    S = np.vstack(sc)
    return S.mean(0) - lam * (S.std(0) if len(S) > 1 else 0.0)


def cr_fuzzy(X, y, k, seed=42, use_assoc=True, use_red=True, lam=1.0, cluster_folds=True, n_clusters=8, n_inner=5):
    A = np.nan_to_num(X.values.astype(float))
    y = np.asarray(y)
    p = A.shape[1]
    rel = _mm(cr_relevance(A, y, seed, n_clusters, n_inner, lam, cluster_folds))
    C = np.nan_to_num(np.corrcoef(A, rowvar=False), nan=0.0)
    np.fill_diagonal(C, 0.0)
    assoc = _mm(np.abs(C).mean(axis=1))
    sel, rem = [], list(range(p))
    for _ in range(min(k, p)):
        red = _mm(np.array([np.abs(C[i, sel]).mean() for i in rem]) if sel else np.zeros(len(rem)))
        a = (1 - assoc[rem]) if use_assoc else np.ones(len(rem))
        d = (1 - red) if use_red else np.ones(len(rem))
        s = rel[rem] * a * d
        j = rem[int(np.argmax(s))]
        sel.append(j); rem.remove(j)
    return sel
