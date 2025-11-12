import argparse, os, pandas as pd, pathlib, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True, help="Direct CSV URL you use in the notebook")
    ap.add_argument("--out", default="data/wisc_bc_diag.csv", help="Where to save the frozen CSV")
    args = ap.parse_args()

    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Read from URL exactly as notebook would
    try:
        df = pd.read_csv(args.url)
    except Exception as e:
        print("Failed to read CSV from URL. If it’s not a pure CSV, try exporting raw link or share URL.", file=sys.stderr)
        raise

    # Save locally (no column changes)
    df.to_csv(out_path, index=False)
    print(f"Saved: {out_path.resolve()}")

    # For quick confirmation, print and save columns
    cols_txt = out_path.with_suffix(".columns.txt")
    cols_txt.write_text("\n".join(map(str, df.columns)), encoding="utf-8")
    print(f"Wrote columns list: {cols_txt.resolve()}")

if __name__ == "__main__":
    main()
