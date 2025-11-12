# agents/__init__.py
"""
Agents package initializer.
Provides stable imports and a convenience EDA wrapper.
"""

from pathlib import Path

# Export primary EDA function
try:
    from .eda_agent import run_eda_report
except Exception as e:
    raise ImportError(f"agents: failed to import run_eda_report from eda_agent: {e}")

# Optional feature engineering helpers
try:
    from .fe_agent import propose_features, apply_features  # noqa: F401
except Exception:
    propose_features = None
    apply_features = None

# Default artifacts directory
EDA_ARTIFACTS_DIR = Path(__file__).resolve().parents[1] / "artifacts" / "eda_reports"

def run_breast_cancer_eda(df, target_col=None, out_dir: str | Path = EDA_ARTIFACTS_DIR):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    return run_eda_report(df=df, target_col=target_col, out_dir=str(out_dir))

__all__ = [
    "run_eda_report",
    "run_breast_cancer_eda",
    "propose_features",
    "apply_features",
    "EDA_ARTIFACTS_DIR",
]
