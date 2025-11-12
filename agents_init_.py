# agents/__init__.py
"""
Agents package initializer.
Exposes EDA wrapper and ensures artifacts path exists.
"""
from pathlib import Path

# Public API imports (soft-fail if optional modules are missing)
try:
    from .eda_agent import run_eda_report
except Exception as e:
    raise ImportError(f"agents: failed to import run_eda_report from eda_agent: {e}")

# Optional helpers
try:
    from .fe_agent import propose_features, apply_features  # noqa: F401
except Exception:
    propose_features = None
    apply_features = None

# Default artifacts directory
EDA_ARTIFACTS_DIR = Path(r"C:\Users\rajni\Documents\breast-cancer-agentic\artifacts\eda_reports")

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
