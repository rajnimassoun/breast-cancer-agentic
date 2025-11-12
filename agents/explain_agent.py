import argparse, os, joblib, pandas as pd, shap
import matplotlib.pyplot as plt
from lime.lime_tabular import LimeTabularExplainer
import yaml

def main(cfg):
    Xte = pd.read_csv("data/processed/X_test.csv")
    model = joblib.load("artifacts/modeling/best_model.pkl")

    os.makedirs("artifacts/explain", exist_ok=True)

    # --- SHAP global feature importance ---
    explainer = shap.Explainer(model.predict_proba, Xte, feature_names=Xte.columns)
    sv = explainer(Xte)

    shap.plots.beeswarm(sv[:, :, 1], show=False)
    plt.tight_layout()
    plt.savefig("artifacts/explain/global_shap.png", dpi=180)
    plt.close()

    # --- LIME local explanations ---
    X_array = Xte.values
    expl = LimeTabularExplainer(
        X_array,
        feature_names=list(Xte.columns),
        discretize_continuous=True,
        mode="classification"
    )

    lime_dir = "artifacts/explain/lime_examples"
    os.makedirs(lime_dir, exist_ok=True)

    for i in range(min(3, len(Xte))):
        exp = expl.explain_instance(X_array[i], model.predict_proba, num_features=8)
        exp.save_to_file(os.path.join(lime_dir, f"lime_{i}.html"))

    # --- Write summary report ---
    with open("artifacts/explain/report.md", "w") as f:
        f.write(
            "# Explainability Report\n\n"
            "- `global_shap.png`: global feature importance summary.\n"
            "- LIME HTMLs in `lime_examples/` show local reasoning for individual cases.\n"
        )

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config.yaml")
    args = ap.parse_args()
    cfg = yaml.safe_load(open(args.config))
    main(cfg)
