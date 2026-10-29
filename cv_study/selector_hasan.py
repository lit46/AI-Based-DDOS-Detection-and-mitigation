"""
selector_hasan.py -- two selectors that encode the claim of Hasan, Eaman & Hassan, Procedia Computer Science 265 (2025) 124-131:
  HASAN_Top5_Published : their published top-5 feature list, applied as-is (ignores k; always 5 features)
  HASAN_XGB_Gain5      : their PROCEDURE (XGBoost, 100 trees, depth 3, lr 0.1, importance ranking) run on our training fold
Honest labelling: the paper trains the ranking model on its whole training set; here, like every other selector in this study,
it sees the stratified selection subsample of the training fold (--fs_rows). Column matching ignores case and punctuation.
"""
import re
import numpy as np

PUBLISHED = {   # paper's name -> accepted normalised spellings (CICFlowMeter / our adapter / paper wording)
    "ACK Flag Count": ["ackflagcount"],
    "Bwd Packets/s": ["bwdpacketss", "bwdpacketspersecond"],
    "URG Flag Count": ["urgflagcount"],
    "Fwd Packet Length Min": ["fwdpacketlengthmin"],
    "Init Fwd Win Bytes": ["initwinbytesforward", "initfwdwinbytes", "initwinbytesfwd"],
}


def _n(c):
    return re.sub(r"[^0-9a-z]", "", str(c).lower())


def resolve(columns):
    """-> ({paper name: column position}, [paper names not found])"""
    norm = {_n(c): i for i, c in enumerate(columns)}
    found, missing = {}, []
    for name, alts in PUBLISHED.items():
        hit = next((norm[a] for a in alts if a in norm), None)
        (found.__setitem__(name, hit) if hit is not None else missing.append(name))
    return found, missing


def hasan_top5_published(X, y, k, seed=42):
    found, missing = resolve(list(X.columns))
    if missing:
        raise ValueError(f"published feature(s) not in the cleaned data: {missing}")
    return list(found.values())


def hasan_xgb_gain(X, y, k, seed=42):
    from xgboost import XGBClassifier
    classes = np.unique(y)
    yy = np.searchsorted(classes, y)                       # contiguous labels even if a class is absent from the subsample
    m = XGBClassifier(n_estimators=100, max_depth=3, learning_rate=0.1, tree_method="hist", n_jobs=1,
                      random_state=seed, verbosity=0, importance_type="gain")
    m.fit(X.values, yy)
    imp = np.asarray(m.feature_importances_, dtype=float)
    return [int(i) for i in np.argsort(imp)[::-1][:k]]
