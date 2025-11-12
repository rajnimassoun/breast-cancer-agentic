import argparse, os, json, joblib, pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score, f1_score, precision_recall_fscore_support, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import yaml

def candidates():
    return {
        "logreg": Pipeline([("scaler", StandardScaler()), ("clf", LogisticRegression(max_iter=2000))]),
        "svm":   Pipeline([("scaler", StandardScaler()), ("clf", SVC(probability=True))]),
        "rf":    Pipeline([("clf", RandomForestClassifier(random_state=42))]),
    }

def main(cfg):
    Xtr = pd.read_csv("data/processed/X_train.csv")
    ytr = pd.read_csv("data/processed/y_train.csv").iloc[:,0]
    Xte = pd.read_csv("data/processed/X_test.csv")
    yte = pd.read_csv("data/processed/y_test.csv").iloc[:,0]

    skf = StratifiedKFold(n_splits=cfg["cv"]["folds"], shuffle=True, random_state=cfg["cv"]["random_state"])
    models = candidates()

    best_name, best_auc = None, -1.0
    per_model = {}
    for name, model in models.items():
        auc_cv = cross_val_score(model, Xtr, ytr, cv=skf, scoring="roc_auc").mean()
        per_model[name] = {"cv_auc_mean": float(auc_cv)}
        if auc_cv > best_auc:
            best_auc, best_name = auc_cv, name

    best = models[best_name].fit(Xtr, ytr)
    proba = best.predict_proba(Xte)[:,1]
    preds = (proba >= 0.5).astype(int)

    auc = roc_auc_score(yte, proba)
    precision, recall, f1, _ = precision_recall_fscore_support(yte, preds, average="binary", zero_division=0)
    cm = confusion_matrix(yte, preds).tolist()

    os.makedirs("artifacts/modeling", exist_ok=True)
    with open("artifacts/modeling/cv_metrics.json","w") as f:
        json.dump({"best_model_name": best_name, **per_model[best_name]}, f, indent=2)
    with open("artifacts/modeling/test_metrics.json","w") as f:
        json.dump({"auc": float(auc), "precision": float(precision), "recall": float(recall), "f1": float(f1), "confusion_matrix": cm}, f, indent=2)
    joblib.dump(best, "artifacts/modeling/best_model.pkl")

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--config", default="config.yaml")
    args = ap.parse_args(); cfg = yaml.safe_load(open(args.config))
    main(cfg)
