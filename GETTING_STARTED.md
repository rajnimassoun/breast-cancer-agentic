# 🚀 Getting Started - Breast Cancer Agentic ML

## Prerequisites

1. **Python 3.8+** installed
2. **Git** (if cloning from repository)
3. **pip** package manager

## Initial Setup

### Step 1: Navigate to Project Directory
```powershell
cd c:\Users\obinn\OneDrive\Documents\GitHub\breast-cancer-agentic
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Verify Setup
```powershell
python main.py --mode test
```

You should see:
- ✓ Package versions displayed
- ✓ Dataset loaded successfully
- ✓ Directory structure verified

## Quick Start Guide

### 🎯 For First-Time Users

**Easiest Way - Windows Batch Script:**
```powershell
.\run.bat
```
Select option from menu and hit Enter!

**Alternative - Python Interactive Menu:**
```powershell
python quickstart.py
```

**Command Line - Full Pipeline:**
```powershell
python main.py --mode full
```

### 🔬 For Researchers & Data Scientists

**Run Complete Analysis:**
```powershell
# Full pipeline with interactive diagnostics
python main.py --mode full

# Or skip interactive session
python main.py --mode full --no-interactive
```

**What This Does:**
1. Loads Wisconsin Breast Cancer dataset
2. Trains 4 models (Logistic Regression, Random Forest, XGBoost, SVM)
3. Performs hyperparameter tuning
4. Runs feature selection (RFECV)
5. Selects best model
6. Generates SHAP explanations
7. Starts interactive diagnostic session

**Expected Runtime:** 5-10 minutes

### 👨‍💻 For Developers

**Run Modular Agent Pipeline:**
```powershell
# Run all stages
python main.py --mode agents --stage all

# Or run individually
python main.py --mode agents --stage eda        # EDA only
python main.py --mode agents --stage modeling   # Modeling only
python main.py --mode agents --stage explain    # Explain only
```

**Run Jupyter Notebooks:**
```powershell
# Run all notebooks (00_eda, 01_eda, etc.)
python main.py --mode notebooks

# Run specific notebook(s)
python main.py --mode notebooks --notebooks notebooks/00_eda.ipynb
```

**What This Does:**
- **EDA Stage**: Exploratory analysis, feature engineering → `artifacts/eda/`
- **Modeling Stage**: Model training, evaluation → `artifacts/modeling/`
- **Explain Stage**: LIME/SHAP explanations → `artifacts/explain/`
- **Notebooks**: Executes Jupyter notebooks with nbconvert, preserving outputs

**Expected Runtime:** 2-5 minutes per stage

## Execution Methods Comparison

| Method | Best For | Difficulty | Features |
|--------|----------|-----------|----------|
| `run.bat` | Windows users, beginners | ⭐ Easy | Menu-driven, no typing |
| `quickstart.py` | Cross-platform, beginners | ⭐ Easy | Python menu, colorful |
| `main.py` | Power users, automation | ⭐⭐ Medium | Full control, scriptable |
| `--mode notebooks` | Notebook users | ⭐⭐ Medium | Execute Jupyter notebooks |
| Direct files | Advanced users, debugging | ⭐⭐⭐ Hard | Maximum flexibility |

## Interactive Session Guide

When you run `--mode full` (default), you'll enter an interactive diagnostic session:

### Features Available:
1. **Manual Input**: Enter patient measurements
2. **Synthetic Patients**: Generate test cases automatically
3. **Predictions**: Get malignancy risk assessment
4. **Explanations**: View SHAP feature importance
5. **Auto-Logging**: Cases saved to `cases/` directory

### Sample Interaction:
```
Enter feature values (or 'exit' to quit)

Enter mean radius: 15.5
Enter mean texture: 18.2
...
[Continues for all features]

Result:
🔴 MALIGNANT (p = 0.8234)

Top SHAP Contributors:
  worst radius (25.3) ↑ risk +0.42
  worst concavity (0.18) ↑ risk +0.28
  mean concave points (0.09) ↑ risk +0.15

Case saved: cases/case_20250129_143052.json
```

### Exiting:
Type `exit` or press `Ctrl+C` at any prompt

## Output Structure

After running, check these directories:

```
breast-cancer-agentic/
├── artifacts/          # Agent pipeline outputs
│   ├── eda/           # EDA results
│   ├── modeling/      # Model metrics
│   └── explain/       # Explanations
│
├── cases/             # Interactive session cases
│   ├── *.json        # Detailed case results
│   └── *.csv         # Tabular format
│
└── data/
    ├── processed/     # Train/test splits
    └── engineered/    # Feature engineering
```

## Common Commands

### Testing & Verification
```powershell
# Quick test
python main.py --mode test

# Check help
python main.py --help

# View version
python main.py --version
```

### Full Pipeline Variations
```powershell
# Interactive (default)
python main.py --mode full

# Batch processing
python main.py --mode full --no-interactive

# Just the word "python main.py" defaults to full mode
python main.py
```

### Agent Pipeline Variations
```powershell
# All stages sequentially
python main.py --mode agents --stage all

# Individual stages
python main.py --mode agents --stage eda
python main.py --mode agents --stage modeling
python main.py --mode agents --stage explain
```

### Original Methods (Still Work)
```powershell
# Direct orchestrator
python orchestrator.py --stage all

# Direct ML script (advanced)
python obiedeh_breast_cancer_agentic_ml.py
```

## Troubleshooting

### Issue: "Python not found"
**Solution:**
```powershell
# Check Python installation
python --version

# If not found, download from python.org
# Make sure to check "Add Python to PATH" during installation
```

### Issue: "Module not found"
**Solution:**
```powershell
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Or install specific package
pip install scikit-learn xgboost shap
```

### Issue: "Permission denied"
**Solution:**
```powershell
# On Windows, run PowerShell as Administrator
# Or change directory permissions
icacls . /grant Users:F /t
```

### Issue: Script hangs or crashes
**Solution:**
```powershell
# Try non-interactive mode
python main.py --mode full --no-interactive

# Or reduce parallelism (edit obiedeh_breast_cancer_agentic_ml.py)
# Change: N_JOBS = -1  to  N_JOBS = 1
```

### Issue: SHAP warnings
**Solution:** These are harmless warnings about feature names. You can ignore them or suppress with:
```powershell
$env:PYTHONWARNINGS="ignore"
python main.py --mode full
```

## Configuration

Edit `config.yaml` to customize:
```yaml
cv:
  folds: 5           # Cross-validation folds
  random_state: 42   # Reproducibility seed

models:
  xgboost:
    n_estimators: [300, 600]
    learning_rate: [0.05, 0.1]
    # Add/modify hyperparameters

output_dir: artifacts  # Change output location
```

## Performance Tips

1. **Use all CPU cores**: Set `N_JOBS=-1` (already default)
2. **Reduce grid search**: Limit hyperparameter combinations in config
3. **Skip stages**: Use agent mode to run only needed stages
4. **Non-interactive**: Use `--no-interactive` for faster batch processing

## Next Steps

### After First Run:
1. ✅ Check `artifacts/` for results
2. 📊 Review model metrics in `artifacts/modeling/test_metrics.json`
3. 🔍 Explore SHAP explanations in `artifacts/explain/`
4. 📝 Read generated reports

### For Development:
1. Modify `config.yaml` for different hyperparameters
2. Run individual stages to test changes
3. Create custom agents in `agents/` directory
4. Add your own models to the pipeline

### For Production:
1. Use `--no-interactive` mode
2. Integrate with CI/CD pipelines
3. Set up automated reporting
4. Deploy as REST API (requires additional work)

## Documentation

- **This file**: Quick start and troubleshooting
- **MAIN_USAGE.md**: Detailed usage guide
- **MAIN_SUMMARY.md**: Technical overview
- **README.md**: Project overview
- **EDA_FE_README.md**: EDA details
- **agents/README.md**: Agent architecture

## Getting Help

1. Run `python main.py --help`
2. Check documentation files listed above
3. Review error messages carefully
4. Try `python main.py --mode test` to diagnose issues

## Success Indicators

You'll know it's working when you see:
- ✅ "Pipeline completed successfully"
- ✅ Metrics displayed for all models
- ✅ Files created in `artifacts/` or `cases/`
- ✅ No error messages or only warnings (SHAP warnings OK)

## Time Estimates

| Operation | Duration |
|-----------|----------|
| Initial setup | 2-5 min |
| Quick test | 10 sec |
| Full pipeline | 5-10 min |
| Agent - EDA | 1-2 min |
| Agent - Modeling | 3-5 min |
| Agent - Explain | 1-2 min |
| Interactive session | User-dependent |

*Times vary based on hardware*

## Final Checklist

Before your first run:
- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] In project root directory
- [ ] Test passed (`python main.py --mode test`)

Now you're ready! Choose your preferred method and run:
```powershell
.\run.bat          # Windows menu
python quickstart.py    # Python menu  
python main.py     # Command line
```

Happy analyzing! 🎉
