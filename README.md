# Breast Cancer Agentic ML Pipeline

A comprehensive machine learning pipeline for breast cancer diagnosis using the Wisconsin Diagnostic Breast Cancer dataset. This project combines exploratory data analysis, multi-model comparison, and advanced explainability techniques to provide accurate predictions with interpretable results.

## 📋 Project Overview

This pipeline delivers a complete end-to-end machine learning solution for breast cancer classification:

- **Exploratory Data Analysis (EDA)** - Comprehensive feature analysis with mutual information ranking and visualization
- **Multi-Model Architecture** - Compares Logistic Regression, Random Forest, XGBoost, and SVM to automatically select the best performer
- **Adaptive Explainability** - Uses SHAP (LinearExplainer/TreeExplainer/KernelExplainer) and LIME for model-agnostic interpretability
- **Interactive Patient Triage** - Real-time diagnostic interface with automated risk assessment and email alerts
- **Production-Ready Pipeline** - Includes data preprocessing, model training, hyperparameter tuning, and deployment

## 🚀 Getting Started

### Prerequisites

- Python 3.8-3.12 (Python 3.13+ not compatible with LIME)
- pip package manager
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/rajnimassoun/breast-cancer-agentic.git
cd breast-cancer-agentic

# Install required packages
pip install -r requirements.txt
```

### Usage

**Interactive Menu (Recommended)**

Launch the menu interface to access both notebooks:

```bash
python main.py
```

Select from:
- **Option 1:** Exploratory Data Analysis (`00_EDA.ipynb`)
- **Option 2:** ML Pipeline with Explainability (`01_Agentic_ML.ipynb`)

**Direct Notebook Execution**

Run notebooks in Jupyter or Google Colab:

```bash
jupyter notebook 00_EDA.ipynb
```

or

```bash
jupyter notebook 01_Agentic_ML.ipynb
```

## 📊 Performance Metrics

### Model Comparison Results

| Model | Test Accuracy | Test AUC | F1 Score | Training Time |
|-------|--------------|----------|----------|---------------|
| Logistic Regression | 98.2% | 0.9954 | 0.986 | Fast |
| Random Forest | 95.6% | 0.9939 | 0.966 | Moderate |
| XGBoost | 94.7% | 0.9934 | 0.959 | Moderate |
| SVM | 98.2% | 0.9937 | 0.986 | Slow |

**Best Model:** Logistic Regression (ROC-AUC: 0.9954)

### Configuration

- **Cross-Validation:** 5-Fold Stratified K-Fold
- **Optimization:** GridSearchCV with automated hyperparameter tuning
- **Explainability Engine:** Model-adaptive SHAP + LIME
  - LinearExplainer → Logistic Regression
  - TreeExplainer → Random Forest, XGBoost
  - KernelExplainer → SVM, other models

### Feature Importance

Top 5 features identified by Mutual Information Score:

| Rank | Feature | MI Score | Description |
|------|---------|----------|-------------|
| 1 | `concave points_worst` | 0.72 | Severity of concave portions |
| 2 | `concavity_worst` | 0.69 | Severity of concave contours |
| 3 | `perimeter_worst` | 0.68 | Largest cell perimeter |
| 4 | `radius_worst` | 0.67 | Largest cell radius |
| 5 | `area_worst` | 0.66 | Largest cell area |

### Output Artifacts

The pipeline generates organized artifacts for analysis and reproducibility:

```
artifacts/
├── eda/
│   ├── describe.csv              # Statistical summaries
│   ├── mutual_info_ranking.csv   # Feature importance rankings
│   └── data/                     # Train/test splits
├── explain/
│   ├── triage_log.csv           # All patient predictions
│   └── lime_examples/           # Per-patient HTML explanations
```

## 🏗️ Project Structure

```text
breast-cancer-agentic/
├── 00_EDA.ipynb                    # Exploratory Data Analysis notebook
├── 01_Agentic_ML.ipynb             # Full ML pipeline with SHAP/LIME
├── main.py                         # Interactive menu launcher
├── config.yaml                     # Configuration settings
├── data/
│   ├── raw/                       # Original breast cancer dataset
│   ├── processed/                 # Train/test splits
│   └── breast_cancer_with_columns.csv
├── artifacts/
│   ├── eda/                       # EDA reports and data splits
│   └── explain/                   # SHAP/LIME explanations
│       └── lime_examples/         # Per-patient LIME HTML files
├── reports/figures/               # Visualization outputs
├── requirements.txt               # Python dependencies
└── requirements-dev.txt           # Development dependencies
```

## 🔬 Pipeline Components

### 1. Data Preprocessing

Robust data preparation ensures model reliability:

- **Missing Value Handling** - Automated imputation strategies
- **Outlier Management** - Percentile-based capping (1st-99th)
- **Feature Scaling** - StandardScaler for normalization
- **Feature Engineering** - Ratio features (worst/mean)
- **Dimensionality Reduction** - Remove high-correlation features (_se columns)

### 2. Multi-Model Training

Compares four distinct algorithms with full hyperparameter optimization:

| Algorithm | Configuration | Use Case |
|-----------|--------------|----------|
| **Logistic Regression** | L2 regularization, max_iter=5000 | Fast, interpretable baseline |
| **Random Forest** | 100-200 trees, max_depth tuning | Ensemble robustness |
| **XGBoost** | Gradient boosting, learning rate optimization | High-performance prediction |
| **SVM** | RBF & linear kernels, C tuning | Non-linear decision boundaries |

**Training Process:**
- GridSearchCV exhaustive parameter search
- 5-fold stratified cross-validation
- ROC-AUC optimization metric
- Automatic best model deployment

### 3. Interpretability Layer

Dual-explainer architecture provides both global and local insights:

**SHAP (Global & Local)**
- Adaptive explainer selection based on model type
- Feature contribution analysis for every prediction
- Top-5 most influential features per case
- Direction and magnitude of feature impact

**LIME (Local)**
- Instance-level explanations
- HTML visualization export
- Human-readable feature importance
- Saved as `lime_{patient_id}.html`

### 4. Patient Triage System

Interactive diagnostic interface with enterprise features:

- **Input Interface** - Guided feature entry with defaults
- **Risk Classification** - LOW/MEDIUM/HIGH based on probability
- **Dual Explanations** - SHAP + LIME for each prediction
- **Alert System** - Automated email for malignant cases
- **Audit Trail** - JSON and CSV logging for compliance
- **Session Management** - Continuous operation with exit command

## 📦 Technical Stack

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|----------|
| Python | 3.8-3.12 | Runtime (3.13+ incompatible with LIME) |
| scikit-learn | Latest | ML models, pipelines, preprocessing |
| xgboost | Latest | Gradient boosting implementation |
| pandas | Latest | Data manipulation and analysis |
| numpy | Latest | Numerical computations |
| shap | ≥0.40 | Model interpretation framework |
| lime | 0.2.x | Local explanation generation |
| matplotlib | Latest | Visualization engine |
| seaborn | Latest | Statistical plotting |
| scipy | Latest | Scientific algorithms |
| jupyter | Latest | Notebook environment |

### Installation

All dependencies are managed via `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 📁 Repository Structure

```
breast-cancer-agentic/
├── 📓 Notebooks
│   ├── 00_EDA.ipynb                # Exploratory analysis
│   └── 01_Agentic_ML.ipynb         # ML pipeline
├── 🐍 Scripts
│   └── main.py                     # Interactive launcher
├── 📊 Data
│   ├── raw/                        # Original dataset
│   ├── processed/                  # Train/test splits
│   └── breast_cancer_with_columns.csv
├── 📈 Artifacts
│   ├── eda/                        # Analysis outputs
│   └── explain/                    # Explanation files
│       └── lime_examples/          # Patient-specific HTML
├── ⚙️ Configuration
│   ├── config.yaml                 # Settings
│   ├── requirements.txt            # Dependencies
│   └── requirements-dev.txt        # Dev tools
└── 📄 Documentation
    ├── README.md                   # This file
    └── LICENSE                     # MIT License
```

## 📝 License

MIT License - see [LICENSE](LICENSE) for full text.

## 👥 Team

**University of San Diego - Applied Artificial Intelligence (AAI-501-G5)**

- **Obinna Edeh** - Pipeline Architecture & Implementation
- **Rajini Massoun** - Model Development & Optimization
- **Nicholas Valles** - Explainability & Evaluation

## 🙏 Acknowledgments

- **Dataset:** Breast Cancer Wisconsin (Diagnostic) from UCI ML Repository
- **Institution:** University of San Diego Applied AI Program
- **Libraries:** scikit-learn, XGBoost, SHAP, LIME development teams

## 📧 Contact

For questions or collaboration:
- Open an issue in this repository
- Course: AAI-501-G5, University of San Diego

---

**Built with ❤️ for advancing interpretable AI in healthcare**

