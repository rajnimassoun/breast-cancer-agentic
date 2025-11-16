"""Minimal example EDA agent for local testing.

This module provides a tiny `run_eda_report` implementation that conforms to
the notebook's agent contract. It supports being called with either an in-
memory DataFrame (`df`) or a `dataset_path` (CSV). The agent writes a small
`summary.txt` into `out_dir` and returns a JSON-serializable dict with
artifact paths so the adapter can validate end-to-end behavior.

Important notes for integrators:
- This is for local testing only and performs no sensitive-data handling.
- Real agents should avoid printing raw PII to stdout and should follow the
  audit and de-identification guidance in `agents/`.
"""

from pathlib import Path
import pandas as pd


def run_eda_report(df=None, dataset_path=None, target_col=None, out_dir=None, **_):
    # Validate inputs: either df or dataset_path must be provided
    if df is None and dataset_path is None:
        raise ValueError("Provide df or dataset_path")
    if df is None:
        # Load CSV when running in subprocess mode
        df = pd.read_csv(dataset_path)

    # Ensure output directory exists and is under the project's artifacts
    out_dir = out_dir or "artifacts/eda/example_agent"
    Path(out_dir).mkdir(parents=True, exist_ok=True)

    # Write a tiny summary file so the parent notebook can check for artifacts
    summary_path = Path(out_dir) / "summary.txt"
    with open(summary_path, "w", encoding="utf-8") as fh:
        fh.write(f"rows={len(df)}\ncols={len(df.columns)}\n")
        if target_col and target_col in df.columns:
            fh.write(f"target_values={df[target_col].value_counts().to_dict()}\n")

    # Return JSON-serializable summary (adapter expects keys like 'out_dir')
    return {"out_dir": str(out_dir), "summary_path": str(summary_path)}
import argparse, os, json, pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path

TARGET_ALIASES = ["diagnosis", "target", "class", "label", "outcome"]

def find_target_col(df, preferred_name: str | None):
    original_cols = list(df.columns)
    # strip only spaces; keep case for saving
    df.columns = [c.strip() for c in df.columns]
    lower_index = {c.lower(): c for c in df.columns}
    # 1) preferred exact / case-insensitive
    if preferred_name:
        if preferred_name in df.columns:
            return preferred_name
        low = preferred_name.strip().lower()
        if low in lower_index:
            return lower_index[low]
    # 2) common aliases
    for alias in TARGET_ALIASES:
        if alias in lower_index:
            return lower_index[alias]
    # 3) heuristic (M/B or 0/1)
    for c in df.columns:
        vals = pd.Series(df[c]).dropna().unique()
        if len(vals) <= 10:
            svals = set(str(v).strip().upper() for v in vals)
            if svals.issubset({"M","B","MALIGNANT","BENIGN","0","1"}):
                return c
    raise KeyError(f"Could not find target column. Columns: {df.columns.tolist()}")

def encode_target(series):
    if series.dtype == "O":
        s = series.astype(str).str.strip().str.upper()
        mapping = {"M":1,"MALIGNANT":1,"1":1,"B":0,"BENIGN":0,"0":0}
        return s.map(mapping).astype(int)
    return series.astype(int)

def resolve_path(p):
    pth = Path(p)
    if pth.exists(): return str(pth)
    for ext in (".csv",".xlsx",".data"):
        if pth.with_suffix(ext).exists():
            return str(pth.with_suffix(ext))
    raise FileNotFoundError(f"Data not found: {p}")

def run(cfg):
    data_path = resolve_path(cfg["data_path"])
    df = pd.read_csv(data_path) if data_path.lower().endswith(".csv") else pd.read_excel(data_path)

    # drop non-feature extras if present
    for col in ["Unnamed: 32", cfg.get("id_col", None)]:
        if col: df = df.drop(columns=[col], errors="ignore")

    target_col = find_target_col(df, cfg.get("target_col"))
    y = encode_target(df[target_col])
    X = df.drop(columns=[target_col])

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    os.makedirs("data/processed", exist_ok=True)
    Xtr.to_csv("data/processed/X_train.csv", index=False)
    Xte.to_csv("data/processed/X_test.csv", index=False)
    ytr.to_csv("data/processed/y_train.csv", index=False)
    yte.to_csv("data/processed/y_test.csv", index=False)

    os.makedirs("artifacts/eda", exist_ok=True)
    summary = {
        "n_samples": int(len(df)),
        "n_features": int(X.shape[1]),
        "detected_target_col": target_col,
        "class_balance": {"benign": int((y==0).sum()), "malignant": int((y==1).sum())},
        "missing": int(df.isna().sum().sum()),
        "recommended_preprocessing": ["StandardScaler"]
    }
    with open("artifacts/eda/eda_summary.json","w") as f:
        json.dump(summary, f, indent=2)

def run_eda_report(df, target_col=None, out_dir="artifacts/eda"):
    """
    Compatibility wrapper for notebook usage.
    - df: pandas DataFrame
    - target_col: optional column name hint
    - out_dir: directory to write artifacts
    Uses existing helper functions to detect/encode target and write simple artifacts.
    """
    from pathlib import Path
    from sklearn.model_selection import train_test_split

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Work on a copy to avoid mutating user's dataframe
    df_local = df.copy()

    # Detect target column (or use provided if valid)
    try:
        tc = find_target_col(df_local, target_col)
    except KeyError:
        if target_col and target_col in df_local.columns:
            tc = target_col
        else:
            raise

    # Encode target and split features
    y = encode_target(df_local[tc])
    X = df_local.drop(columns=[tc])

    # Create simple train/test splits
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    # Write data CSVs under out_dir/data
    data_dir = out_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    Xtr.to_csv(data_dir / "X_train.csv", index=False)
    Xte.to_csv(data_dir / "X_test.csv", index=False)
    ytr.to_csv(data_dir / "y_train.csv", index=False)
    yte.to_csv(data_dir / "y_test.csv", index=False)

    # Write a small summary JSON
    summary = {
        "n_samples": int(len(df_local)),
        "n_features": int(X.shape[1]),
        "detected_target_col": tc,
        "class_balance": {"benign": int((y==0).sum()), "malignant": int((y==1).sum())},
        "missing": int(df_local.isna().sum().sum()),
        "recommended_preprocessing": ["StandardScaler"]
    }
    with open(out_dir / "eda_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Additional quick artifacts
    df_local.head(50).to_csv(out_dir / "sample_rows.csv", index=False)
    df_local.describe(include="all").T.to_csv(out_dir / "describe.csv")
    df_local.isna().sum().sort_values(ascending=False).to_csv(out_dir / "missing_counts.csv")

    return {"summary_path": str(out_dir / "eda_summary.json"), "out_dir": str(out_dir)}

if __name__ == "__main__":
    import yaml
    ap = argparse.ArgumentParser(); ap.add_argument("--config", default="config.yaml")
    args = ap.parse_args(); cfg = yaml.safe_load(open(args.config))
    run(cfg)
