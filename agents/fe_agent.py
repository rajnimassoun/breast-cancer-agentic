import pandas as pd

def propose_features(X: pd.DataFrame, y=None, max_interactions: int = 20):
    """
    Return a list of feature proposals. Minimal stub returns an empty list.
    Each proposal could be a dict like {"name": "feat_x_y", "type": "interaction", "cols": ["x","y"]}.
    """
    return []

def apply_features(X: pd.DataFrame, proposals):
    """
    Apply proposals to X and return (X_new, metadata). Minimal stub returns X unchanged.
    """
    return X.copy(), {"applied": [], "count": 0}
