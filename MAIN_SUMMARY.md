# Breast Cancer Agentic ML - Main Entry Point Summary

## 📋 What Was Created

Three new files have been added to provide a unified entry point for running the breast cancer ML pipeline:

### 1. `main.py` - Main Entry Point Script
**Location:** `c:\Users\obinn\OneDrive\Documents\GitHub\breast-cancer-agentic\main.py`

A comprehensive Python script that provides three execution modes:

#### **Full Mode** (Default)
Runs the complete ML pipeline from `obiedeh_breast_cancer_agentic_ml.py`:
- Loads breast cancer dataset
- Trains multiple models (Logistic Regression, Random Forest, XGBoost, SVM)
- Performs hyperparameter tuning with GridSearchCV
- Runs Recursive Feature Elimination (RFECV)
- Selects best model based on performance
- Sets up SHAP explainer for interpretability
- Launches interactive patient diagnostic session

#### **Agent Mode**
Runs the modular agent-based pipeline via `orchestrator.py`:
- EDA Agent: Exploratory data analysis
- Modeling Agent: Model training and evaluation
- Explain Agent: Model explanation and interpretability

#### **Test Mode**
Quick setup verification:
- Tests package imports
- Verifies data loading
- Checks directory structure

### 2. `MAIN_USAGE.md` - Detailed Usage Documentation
**Location:** `c:\Users\obinn\OneDrive\Documents\GitHub\breast-cancer-agentic\MAIN_USAGE.md`

Complete documentation including:
- Prerequisites and setup
- All execution modes with examples
- Command-line options reference
- Interactive session features
- Output artifacts description
- Troubleshooting guide
- Configuration options
- Architecture overview

### 3. `quickstart.py` - Interactive Menu Script
**Location:** `c:\Users\obinn\OneDrive\Documents\GitHub\breast-cancer-agentic\quickstart.py`

User-friendly interactive menu for running the pipeline without remembering commands:
- Menu-driven interface
- 7 preset options covering all use cases
- Built-in error handling
- Easy navigation

### 4. Updated `README.md`
Added quick start section with multiple run options and link to detailed documentation.

## 🚀 How to Use

### Option 1: Command Line (Recommended for Power Users)

```powershell
# Run full pipeline with interactive session
python main.py --mode full

# Run full pipeline without interaction
python main.py --mode full --no-interactive

# Run all agent stages
python main.py --mode agents --stage all

# Run specific agent stage
python main.py --mode agents --stage eda

# Test your setup
python main.py --mode test

# View all options
python main.py --help
```

### Option 2: Interactive Menu (Easiest)

```powershell
python quickstart.py
```

This launches an interactive menu where you can:
1. Select from preset options (1-7)
2. Let the script build the command for you
3. See results and return to menu
4. No need to remember command syntax

### Option 3: Direct Execution (Original Method)

```powershell
# Run orchestrator directly
python orchestrator.py --stage all

# Run the ML script directly
python obiedeh_breast_cancer_agentic_ml.py
```

## 📊 Execution Flow

### Full Mode Flow
```
main.py (--mode full)
    ↓
obiedeh_breast_cancer_agentic_ml.py
    ├── 1. Load Data
    ├── 2. Train Models (LR, RF, XGBoost, SVM)
    ├── 3. RFECV + Optimization
    ├── 4. Select Best Model
    ├── 5. Setup SHAP
    └── 6. Interactive Session (optional)
         ├── Manual input
         ├── Synthetic patients
         ├── Real-time predictions
         ├── SHAP explanations
         └── Auto-save cases
```

### Agent Mode Flow
```
main.py (--mode agents)
    ↓
orchestrator.py
    ├── EDA Agent → artifacts/eda/
    ├── Modeling Agent → artifacts/modeling/
    └── Explain Agent → artifacts/explain/
```

## 🎯 Key Features

### Command-Line Interface
- **Unified entry point**: One script for all execution modes
- **Flexible options**: Choose interactive or batch mode
- **Help system**: Built-in `--help` for all options
- **Error handling**: Graceful error messages and recovery

### Interactive Menu
- **User-friendly**: No command-line knowledge needed
- **Visual feedback**: Clear status messages and colors
- **Easy navigation**: Simple number selection
- **Persistent**: Return to menu after each operation

### Full Pipeline Mode
- **End-to-end ML**: Complete workflow automation
- **Model comparison**: Multiple algorithms evaluated
- **Hyperparameter tuning**: Automated optimization
- **Feature selection**: RFECV for optimal features
- **Interpretability**: SHAP-based explanations
- **Interactive diagnostics**: Real-time patient assessment

### Agent Pipeline Mode
- **Modular design**: Run stages independently
- **Configuration-driven**: Customize via `config.yaml`
- **Artifact generation**: Structured output for each stage
- **Reproducible**: Consistent results across runs

## 📁 Output Artifacts

### Full Mode Outputs
```
cases/
├── case_20250129_143052.json    # Individual case results
└── case_20250129_143052.csv     # Tabular format
```

### Agent Mode Outputs
```
artifacts/
├── eda/
│   ├── eda_summary.json
│   ├── describe.csv
│   ├── missing_counts.csv
│   ├── mutual_info_ranking.csv
│   └── data/
│       ├── X_train.csv
│       ├── X_test.csv
│       ├── y_train.csv
│       └── y_test.csv
├── modeling/
│   ├── cv_metrics.json
│   └── test_metrics.json
└── explain/
    ├── report.md
    └── lime_examples/
        ├── lime_0.html
        ├── lime_1.html
        └── lime_2.html
```

## 🔧 Command Reference

| Command | Description |
|---------|-------------|
| `python main.py` | Run full pipeline (default) |
| `python main.py --mode full` | Explicit full mode |
| `python main.py --mode full --no-interactive` | Batch mode |
| `python main.py --mode agents --stage all` | All agent stages |
| `python main.py --mode agents --stage eda` | EDA only |
| `python main.py --mode agents --stage modeling` | Modeling only |
| `python main.py --mode agents --stage explain` | Explain only |
| `python main.py --mode test` | Quick test |
| `python main.py --help` | Show help |
| `python main.py --version` | Show version |
| `python quickstart.py` | Interactive menu |

## 🐛 Troubleshooting

### "ModuleNotFoundError"
```powershell
pip install -r requirements.txt --upgrade
```

### "File not found" errors
Ensure you're in the project root directory:
```powershell
cd c:\Users\obinn\OneDrive\Documents\GitHub\breast-cancer-agentic
```

### Permission errors
Check you have write permissions for the directory.

### Test mode fails
Run: `python main.py --mode test` to identify specific issues.

## 💡 Best Practices

1. **First time setup**: Run `python main.py --mode test` to verify everything works
2. **Development**: Use `--mode agents --stage <stage>` to test individual components
3. **Production**: Use `--mode full --no-interactive` for automated runs
4. **Learning**: Use `--mode full` to explore the interactive session
5. **Quick access**: Use `python quickstart.py` for the easiest experience

## 📚 Documentation

- **Quick reference**: This file
- **Detailed guide**: `MAIN_USAGE.md`
- **Project overview**: `README.md`
- **EDA details**: `EDA_FE_README.md`
- **Agent info**: `agents/README.md`

## ✅ Verification

Test that everything is working:

```powershell
# 1. Test the setup
python main.py --mode test

# 2. Try the interactive menu
python quickstart.py

# 3. Run a quick agent stage
python main.py --mode agents --stage eda
```

## 🎓 Examples

### Example 1: Complete Workflow
```powershell
# Test setup
python main.py --mode test

# Run full pipeline
python main.py --mode full

# Follow prompts in interactive session
# Type 'exit' when done
```

### Example 2: Development Workflow
```powershell
# Run EDA
python main.py --mode agents --stage eda

# Check outputs
Get-ChildItem artifacts\eda\

# Run modeling
python main.py --mode agents --stage modeling

# Run explanation
python main.py --mode agents --stage explain
```

### Example 3: Batch Processing
```powershell
# Run without interaction (for CI/CD)
python main.py --mode full --no-interactive

# Check results were generated
Get-ChildItem artifacts\
```

## 🎉 Summary

You now have three ways to run the breast cancer ML pipeline:

1. **`main.py`**: Powerful command-line interface with multiple modes
2. **`quickstart.py`**: Easy interactive menu for all operations  
3. **Direct execution**: Original method for advanced users

All methods produce the same high-quality results with comprehensive model training, evaluation, and interpretability features.

Choose the method that best fits your workflow!
