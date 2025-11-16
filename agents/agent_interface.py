"""Agent interface specification for local `agents/` implementations.

Place this file under `agents/` as a reference for contributors. It declares
lightweight Protocols and example implementations so agent authors know the
expected function names, signatures, and return shapes.

Notes:
- `run_eda_report` may accept either an in-memory `df` (pandas.DataFrame) or a
  file path via `dataset_path`/`path`. Implementations should support at least
  one of those calling styles.
- Implementations should write artifacts into the provided `out_dir` and
  return a JSON-serializable dictionary with at least `out_dir` and/or
  `summary_path` keys.
"""
from typing import Protocol, Any, Dict, Optional, List, Tuple
from dataclasses import dataclass
from pathlib import Path

# Lightweight result dataclass for documentation purposes only; agents may
# return plain dicts as long as they're JSON-serializable.
@dataclass
class EDAResult:
    summary_path: Optional[str]
    out_dir: str
    metadata: Dict[str, Any] = None


class EDAAgentProtocol(Protocol):
    def run_eda_report(self,
                       df: Optional[Any] = None,
                       dataset_path: Optional[str] = None,
                       target_col: Optional[str] = None,
                       out_dir: Optional[str] = None,
                       **kwargs) -> Dict[str, Any]:
        """Run exploratory data analysis.

        Expected behavior:
        - Accepts either `df` (pandas.DataFrame) OR `dataset_path` (str/path).
        - Writes any output artifacts into `out_dir` (string path).
        - Returns a JSON-serializable dict with at least `out_dir` and/or
          `summary_path` keys.

        Example return value:
            {"out_dir": "artifacts/eda/agent123", "summary_path": "artifacts/eda/agent123/report.html"}
        """
        ...


class FEAgentProtocol(Protocol):
    def propose_features(self,
                         X: Any,
                         y: Optional[Any] = None,
                         max_interactions: int = 20) -> List[Dict[str, Any]]:
        """Return a list of feature proposal objects.

        Proposal format is intentionally lightweight and project-specific, but an
        example element could be:
            {"name": "ratio_perimeter_area", "type": "derived", "expr": "area_worst / perimeter_mean"}
        """

    def apply_features(self,
                       X: Any,
                       proposals: List[Dict[str, Any]],
                       dry_run: bool = False) -> Tuple[Any, Dict[str, Any]]:
        """Apply selected proposals to `X` and return (X_new, metadata).

        - If `dry_run==True`, do not persist changes to disk and return the
          transformed DataFrame plus metadata describing intended changes.
        - Metadata should include an `applied` list with names and a `count`.
        """
        ...


# --- Minimal example implementations (for local testing / examples) ---
# These are intentionally simple and should not be used as production agents.

def example_run_eda_report(df=None, dataset_path=None, target_col=None, out_dir=None, **_):
    """Very small example that demonstrates the contract.

    - If called with `dataset_path`, loads CSV.
    - Writes a tiny `summary.txt` into `out_dir` and returns a dict.
    """
    import os
    import pandas as pd

    if df is None and dataset_path is None:
        raise ValueError("Provide either `df` or `dataset_path`")

    if df is None:
        df = pd.read_csv(dataset_path)

    out_dir = out_dir or "artifacts/eda/example"
    os.makedirs(out_dir, exist_ok=True)
    summary_path = str(Path(out_dir) / "summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(f"rows={len(df)}\ncols={len(df.columns)}\n")

    return {"summary_path": summary_path, "out_dir": out_dir}
