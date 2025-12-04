# Breast Cancer Agentic ML Pipeline

An agentic machine learning pipeline for the Breast Cancer Wisconsin (Diagnostic) dataset featuring deep exploratory data analysis, XGBoost modeling with hyperparameter tuning, and SHAP/LIME explainability.

## 📋 Project Overview

This project implements a complete ML workflow for breast cancer diagnosis using:

- **Exploratory Data Analysis (EDA)** with feature engineering and mutual information ranking
- **XGBoost Classification** with GridSearchCV hyperparameter optimization
- **Model Explainability** using SHAP for global interpretability and LIME for local explanations
- **Interactive Diagnostic Interface** for real-time patient predictions

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/rajnimassoun/breast-cancer-agentic.git
cd breast-cancer-agentic

# Install dependencies
pip install -r requirements.txt
```

### Run the Pipeline

#### Option 1: Simple Menu Interface (Recommended)

```bash
python main.py
```

This opens an interactive menu where you can:

1. Run 00_EDA Notebook (Exploratory Data Analysis)
2. Run 01_Agentic_ML Notebook (Interactive ML Pipeline)

#### Option 2: Direct Notebook Execution

Open notebooks in Google Colab or Jupyter:

- `00_EDA.ipynb` - Complete EDA with feature engineering
- `01_Agentic_ML.ipynb` - Full ML pipeline with XGBoost and explainability

#### Option 3: Python Script

```bash
python 01_Agentic_ML.py
```

## 📊 Results

### Model Performance

- **Best Model:** XGBoost Classifier
- **Test ROC-AUC:** ~0.99
- **Cross-Validation:** Stratified K-Fold (k=3)
- **Hyperparameter Tuning:** GridSearchCV over 243 parameter combinations

### Key Features Identified

Top features by Mutual Information:

1. `concave points_worst`
2. `concavity_worst`
3. `perimeter_worst`
4. `radius_worst`
5. `area_worst`

### Artifacts Generated

- `artifacts/eda/` - EDA reports, mutual information rankings, train/test splits
- `artifacts/engineering/` - Feature transformers and scalers
- `artifacts/modeling/` - Model metrics and performance reports
- `artifacts/explain/` - SHAP plots and LIME explanations
- `cases/` - Patient diagnostic session logs

## 🏗️ Project Structure

```text
breast-cancer-agentic/
├── 00_EDA.ipynb              # Exploratory Data Analysis notebook
├── 01_Agentic_ML.ipynb       # Full ML pipeline notebook
├── 01_Agentic_ML.py          # Python script version
├── main.py                   # Simple menu interface
├── agents/                   # Agent modules
│   ├── eda_agent.py         # EDA automation
│   ├── fe_agent.py          # Feature engineering
│   ├── modeling_agent.py    # Model training
│   ├── explain_agent.py     # SHAP/LIME explainability
│   ├── audit_logger.py      # Audit logging
│   └── privacy.py           # De-identification utilities
├── data/
│   ├── raw/                 # Original dataset
│   ├── processed/           # Train/test splits
│   └── engineered/          # Feature-engineered data
├── artifacts/               # Generated reports and metrics
├── cases/                   # Patient diagnostic logs
└── requirements.txt         # Python dependencies
```

## 🔬 Features

### Data Processing

- Automated missing value imputation
- Percentile-based outlier capping (1st-99th percentiles)
- StandardScaler normalization
- Ratio feature engineering (worst/mean ratios)
- Removal of standard error (_se) columns

### Modeling

- XGBoost with tree_method='hist' for efficiency
- GridSearchCV hyperparameter optimization
- Stratified K-Fold cross-validation
- Multiple evaluation metrics (ROC-AUC, F1, Precision, Recall)

### Explainability

- **SHAP (SHapley Additive exPlanations):** Global feature importance
- **LIME (Local Interpretable Model-agnostic Explanations):** Individual prediction explanations
- Confusion matrix visualization
- Feature correlation heatmaps

### Safety & Privacy

- Audit logging for all operations
- De-identification utilities for sensitive data
- Subprocess isolation for agent execution
- Configurable timeout protection

## 📦 Dependencies

- Python 3.8+
- XGBoost
- scikit-learn
- pandas
- numpy
- matplotlib
- seaborn
- SHAP
- LIME
- joblib

See `requirements.txt` for complete list.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Obinna Edeh** - USD - AAI - 501 - G5

## 🙏 Acknowledgments

- Breast Cancer Wisconsin (Diagnostic) dataset from UCI Machine Learning Repository
- USD Applied Artificial Intelligence program

