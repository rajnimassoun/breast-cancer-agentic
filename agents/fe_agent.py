"""Minimal example feature-engineering agent for local testing.

This module provides simple `propose_features` and `apply_features`
implementations to exercise the notebook adapter's feature-engineering paths.

DO NOT use this code in production. It is intentionally trivial and exists
to demonstrate the agent contract and to provide testable behavior for the
adapter (dry-run support, metadata shape).
"""

from typing import List, Dict, Any, Tuple


def propose_features(X, y=None, max_interactions=20) -> List[Dict[str, Any]]:
    """Return a tiny list of proposed features.

    The proposals are intentionally simple: pick the first two numeric
    columns and suggest their ratio. Real agents should return richer,
    validated proposals with transformation details.
    """
    cols = list(X.select_dtypes(include=["number"]).columns)
    proposals = []
    if len(cols) >= 2:
        proposals.append({
            "name": f"{cols[0]}_over_{cols[1]}",
            "type": "derived",
            "expr": f"{cols[0]} / {cols[1]}",
        })
    return proposals


def apply_features(X, proposals, dry_run=True, confirm=False) -> Tuple[Any, Dict[str, Any]]:
    """Apply proposals to `X` and return (X_new, metadata).

    This naive implementation creates placeholder columns and returns
    metadata describing which proposals were applied. The `dry_run`
    parameter is respected; when True no side effects occur.
    """
    X_new = X.copy()
    applied = []
    for p in proposals or []:
        name = p.get("name") if isinstance(p, dict) else str(p)
        # Example behavior: create a placeholder column so downstream code
        # can validate that the feature exists. Replace with real logic.
        X_new[name] = 0
        applied.append(name)

    metadata = {"applied": applied, "count": len(applied)}
    return X_new, metadata
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
