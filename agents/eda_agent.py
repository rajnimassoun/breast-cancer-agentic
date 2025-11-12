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

if __name__ == "__main__":
    import yaml
    ap = argparse.ArgumentParser(); ap.add_argument("--config", default="config.yaml")
    args = ap.parse_args(); cfg = yaml.safe_load(open(args.config))
    run(cfg)
