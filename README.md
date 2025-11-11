# breast-cancer-agentic
Agentic ML pipeline for Breast Cancer Wisconsin (Diagnostic): deep EDA, model comparison, and explainability.

# breast-cancer-agentic
Agentic ML pipeline for Breast Cancer Wisconsin (Diagnostic): deep EDA, model comparison, and explainability.

## Results (So Far)
- **Detected target:** (from `artifacts/eda/eda_summary.json`)
- **Best model:** (from `artifacts/modeling/cv_metrics.json`)
- **Test metrics:** (from `artifacts/modeling/test_metrics.json`)  
  - AUC: …
  - F1: …
  - Precision / Recall: … / …
- **Explainability:** `artifacts/explain/global_shap.png` shows top features for the malignant class;  
  LIME HTML files in `lime_examples/` explain 3 individual predictions.

## Reproduce
```bash
pip install -r requirements.txt
python orchestrator.py --stage all

