# breast-cancer-agentic
Agentic ML pipeline for Breast Cancer Wisconsin (Diagnostic): deep EDA, model comparison, and explainability.

## Quick Start

### Option 1: Run Full ML Pipeline (Recommended)
```bash
# Install dependencies
pip install -r requirements.txt

# Run the complete pipeline with interactive session
python main.py --mode full

# Or run without interactive session
python main.py --mode full --no-interactive
```

### Option 2: Run Agent-Based Pipeline
```bash
# Run all stages
python main.py --mode agents --stage all

# Or run individual stages
python main.py --mode agents --stage eda
python main.py --mode agents --stage modeling
python main.py --mode agents --stage explain
```

### Option 3: Direct Orchestrator (Original Method)
```bash
python orchestrator.py --stage all
```

**📖 For detailed usage instructions, see [MAIN_USAGE.md](MAIN_USAGE.md)**

## Results (So Far)
- **Detected target:** (from `artifacts/eda/eda_summary.json`)
- **Best model:** (from `artifacts/modeling/cv_metrics.json`)
- **Test metrics:** (from `artifacts/modeling/test_metrics.json`)  
  - AUC: …
  - F1: …
  - Precision / Recall: … / …
- **Explainability:** `artifacts/explain/global_shap.png` shows top features for the malignant class;  
  LIME HTML files in `lime_examples/` explain 3 individual predictions.

## Features

### Full ML Pipeline Mode
- Complete end-to-end machine learning workflow
- Multiple model training and comparison (Logistic Regression, Random Forest, XGBoost, SVM)
- Automated hyperparameter tuning with GridSearchCV
- Recursive Feature Elimination with Cross-Validation (RFECV)
- SHAP-based model interpretability
- Interactive patient diagnostic session
- Automatic case logging and alerts

### Agent-Based Pipeline Mode
- Modular agent architecture (EDA, Modeling, Explanation)
- Independent execution of pipeline stages
- Structured artifact generation
- Configuration-driven workflow

