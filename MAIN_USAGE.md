# Main Entry Point - Usage Guide

## Overview

`main.py` is the unified entry point for the Breast Cancer Agentic ML Pipeline. It provides multiple execution modes to run the complete machine learning workflow, agent-based stages, or quick tests.

## Prerequisites

Ensure you have installed all dependencies:

```powershell
pip install -r requirements.txt
```

## Execution Modes

### 1. Full ML Pipeline (Recommended)

Run the complete machine learning pipeline with interactive session:

```powershell
python main.py --mode full
```

This will:
1. Load the Wisconsin Breast Cancer dataset
2. Train and tune multiple models (Logistic Regression, Random Forest, XGBoost, SVM)
3. Run Recursive Feature Elimination with Cross-Validation (RFECV)
4. Select the best model based on performance metrics
5. Set up SHAP explainer for interpretability
6. Start an interactive agent session for patient diagnostics

### 2. Full Pipeline (Non-Interactive)

Run the pipeline without the interactive session:

```powershell
python main.py --mode full --no-interactive
```

Useful for automated runs, testing, or when you only need model training.

### 3. Agent-Based Pipeline

Run the modular agent-based pipeline using the orchestrator:

#### Run All Stages
```powershell
python main.py --mode agents --stage all
```

#### Run Individual Stages
```powershell
# Exploratory Data Analysis
python main.py --mode agents --stage eda

# Model Training
python main.py --mode agents --stage modeling

# Model Explanation
python main.py --mode agents --stage explain
```

### 4. Jupyter Notebooks

Run all Jupyter notebooks sequentially:

```powershell
# Run all notebooks (00_eda.ipynb, 01_eda.ipynb, etc.)
python main.py --mode notebooks

# Run specific notebook(s)
python main.py --mode notebooks --notebooks notebooks/00_eda.ipynb
python main.py --mode notebooks --notebooks notebooks/00_eda.ipynb notebooks/01_eda.ipynb
```

This will execute the notebooks using nbconvert, preserving outputs in place.

### 5. Quick Test

Verify your setup and environment:

```powershell
python main.py --mode test
```

This checks:
- Required Python packages are installed
- Data can be loaded successfully
- Directory structure is correct

## Command-Line Options

| Option | Choices | Default | Description |
|--------|---------|---------|-------------|
| `--mode` | `full`, `agents`, `notebooks`, `test` | `full` | Execution mode |
| `--stage` | `eda`, `modeling`, `explain`, `all` | `all` | Stage to run (agents mode only) |
| `--no-interactive` | flag | `false` | Skip interactive session |
| `--notebooks` | list of paths | all | Specific notebooks to run (notebooks mode only) |
| `--version` | flag | - | Show version information |

## Interactive Session Features

When running in `full` mode (default), the interactive session provides:

1. **Manual Feature Input**: Enter patient measurements manually
2. **Synthetic Patient Generation**: Generate test cases from the dataset
3. **Real-time Predictions**: Get malignancy predictions with confidence scores
4. **SHAP Explanations**: View feature importance and decision drivers
5. **Case Logging**: Automatic saving of all diagnostic cases
6. **Email Alerts**: Simulated alerts for high-risk cases

### Interactive Commands

- Type patient feature values when prompted
- Enter `exit` to quit the interactive session
- Cases are automatically saved to `cases/` directory

## Output Artifacts

The pipeline generates various artifacts:

```
artifacts/
├── eda/                    # EDA outputs (from agent mode)
│   ├── eda_summary.json
│   ├── describe.csv
│   └── data/
├── modeling/               # Model outputs
│   ├── cv_metrics.json
│   └── test_metrics.json
└── explain/                # Explanation outputs
    ├── report.md
    └── lime_examples/

cases/                      # Interactive session cases (full mode)
├── case_YYYYMMDD_HHMMSS.json
└── case_YYYYMMDD_HHMMSS.csv
```

## Examples

### Example 1: Quick Start
```powershell
# Test your setup
python main.py --mode test

# Run the full pipeline
python main.py --mode full
```

### Example 2: Development Workflow
```powershell
# Run EDA only
python main.py --mode agents --stage eda

# Review results in artifacts/eda/

# Run modeling
python main.py --mode agents --stage modeling

# Run explanation
python main.py --mode agents --stage explain
```

### Example 3: Automated Workflow
```powershell
# Run full pipeline without interaction (for CI/CD)
python main.py --mode full --no-interactive
```

## Troubleshooting

### Import Errors
If you encounter import errors:
```powershell
pip install -r requirements.txt --upgrade
```

### Missing Files
Ensure these files exist:
- `obiedeh_breast_cancer_agentic_ml.py`
- `orchestrator.py`
- `config.yaml`
- `requirements.txt`

### Directory Permissions
If you get permission errors, the script will create directories automatically. Ensure you have write permissions in the project folder.

### SHAP Warnings
SHAP may show warnings about feature names. These can be safely ignored.

## Configuration

Edit `config.yaml` to customize:
- Data paths
- Model hyperparameters
- Cross-validation settings
- Output directories

## Architecture

```
main.py
├── Full Mode
│   └── obiedeh_breast_cancer_agentic_ml.py
│       ├── Data Loading
│       ├── Model Training
│       ├── Feature Selection
│       ├── Model Selection
│       ├── SHAP Setup
│       └── Interactive Session
│
└── Agent Mode
    └── orchestrator.py
        ├── EDA Agent (agents/eda_agent.py)
        ├── Modeling Agent (agents/modeling_agent.py)
        └── Explain Agent (agents/explain_agent.py)
```

## Performance Notes

- **Full Mode**: Takes ~5-10 minutes depending on hardware
- **Agent Mode**: Each stage takes ~2-5 minutes
- **Interactive Session**: Real-time predictions (< 1 second)
- Set `N_JOBS=-1` in the ML script to use all CPU cores

## Support

For issues or questions:
1. Check this README
2. Review the code documentation
3. Check the project README.md
4. Examine error messages carefully

## Version

Current version: 1.0  
Author: Obinna Edeh  
Course: USD - AAI - 501 - G5
