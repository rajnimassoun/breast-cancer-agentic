# Notebook Integration Update Summary

## What Was Added

The `main.py` entry point has been updated to include **Jupyter Notebook execution mode**, allowing you to run all notebook files (`00_eda.ipynb`, `01_eda.ipynb`, etc.) directly from the command line.

## New Features

### 1. Notebook Execution Mode

Execute Jupyter notebooks programmatically using nbconvert:

```powershell
# Run all notebooks in the project
python main.py --mode notebooks

# Run specific notebook(s)
python main.py --mode notebooks --notebooks notebooks/00_eda.ipynb
python main.py --mode notebooks --notebooks notebooks/00_eda.ipynb notebooks/01_eda.ipynb
```

### 2. Automatic Jupyter Installation

If Jupyter/nbconvert is not installed, the script will automatically install it for you.

### 3. Progress Tracking

The notebook execution provides:
- Progress indicators (Notebook 1/4, 2/4, etc.)
- Success/failure status for each notebook
- Error messages if execution fails
- Execution timeout (10 minutes per notebook)

### 4. In-Place Execution

Notebooks are executed in-place, meaning:
- All outputs are saved back to the original notebook file
- You can review results directly in Jupyter or VS Code
- No separate output files are created

## Available Notebooks

The following notebooks are automatically detected and can be executed:

1. **`notebooks/00_eda.ipynb`** - Initial exploratory data analysis
2. **`notebooks/01_eda.ipynb`** - Extended EDA
3. **`00_eda (1).ipynb`** - Root-level EDA notebook
4. **`obiedeh_breast_cancer_agentic_ML.ipynb`** - Full ML pipeline notebook

## Updated Interfaces

### Command Line (main.py)

New mode added:
```powershell
python main.py --mode notebooks              # All notebooks
python main.py --mode notebooks --notebooks <path>  # Specific notebook
```

### Interactive Menu (quickstart.py)

Updated to include:
- **Option 7**: Run Jupyter Notebooks (00_eda, 01_eda, etc.)

Menu now has options 0-8 instead of 0-7.

### Batch Script (run.bat)

Updated Windows menu:
- **Option 7**: Run Jupyter Notebooks
- Reorganized to accommodate new option

## Use Cases

### Use Case 1: Run All Notebooks
```powershell
# Execute all notebooks in sequence
python main.py --mode notebooks
```

**When to use:**
- First-time exploration of the data
- Regenerating all notebook outputs
- Comprehensive analysis

### Use Case 2: Run Specific Notebook
```powershell
# Run only the EDA notebook
python main.py --mode notebooks --notebooks notebooks/00_eda.ipynb
```

**When to use:**
- Testing a specific analysis
- Updating one notebook's outputs
- Debugging a particular notebook

### Use Case 3: Interactive Selection
```powershell
# Use the menu system
python quickstart.py
# Select option 7
```

**When to use:**
- Don't want to remember commands
- Visual menu preferred
- Exploring different options

## Technical Details

### Execution Method

The notebook mode uses Jupyter's `nbconvert` tool with the following parameters:
- `--to notebook`: Output format is notebook
- `--execute`: Execute all cells
- `--inplace`: Save outputs to the original file
- Timeout: 600 seconds (10 minutes) per notebook

### Error Handling

The system handles:
- Missing Jupyter installation (auto-installs)
- Non-existent notebook files (skips with warning)
- Execution failures (reports error, continues to next)
- Timeouts (reports timeout, continues to next)

### Dependencies

Required for notebook execution:
- `jupyter` - Jupyter core
- `nbconvert` - Notebook conversion tool
- `nbformat` - Notebook file format

These are automatically installed if missing.

## Integration with Existing Modes

The notebook mode complements existing execution modes:

```
Mode Options:
├── full         - Complete ML pipeline with interactive session
├── agents       - Modular agent-based pipeline (EDA, Modeling, Explain)
├── notebooks    - Execute Jupyter notebooks [NEW]
└── test         - Quick setup verification
```

All modes can be combined in your workflow:

```powershell
# 1. Run notebooks for exploratory analysis
python main.py --mode notebooks

# 2. Run agent pipeline for structured analysis
python main.py --mode agents --stage all

# 3. Run full pipeline for final model
python main.py --mode full
```

## Updated Documentation

The following files have been updated:

1. **`main.py`**
   - Added `run_notebooks()` function
   - Added `--mode notebooks` option
   - Added `--notebooks` argument for specific notebooks
   - Updated help text with examples

2. **`quickstart.py`**
   - Added option 7 for notebooks
   - Updated menu display
   - Changed input range to 0-8

3. **`run.bat`**
   - Added option 7 for notebooks
   - Added `:NOTEBOOKS` label
   - Updated menu structure

4. **`MAIN_USAGE.md`**
   - Added "Jupyter Notebooks" section
   - Updated command-line options table
   - Added notebook examples

5. **`GETTING_STARTED.md`**
   - Added notebook execution instructions
   - Updated execution methods comparison table
   - Added notebook use case

## Quick Reference

### All Ways to Run Notebooks

```powershell
# Method 1: Command line - All notebooks
python main.py --mode notebooks

# Method 2: Command line - Specific notebook
python main.py --mode notebooks --notebooks notebooks/00_eda.ipynb

# Method 3: Interactive Python menu
python quickstart.py
# Choose option 7

# Method 4: Windows batch menu
.\run.bat
# Choose option 7

# Method 5: Direct (original method)
jupyter nbconvert --execute --inplace notebooks/00_eda.ipynb
```

## Benefits

1. **Convenience**: Run notebooks without opening Jupyter
2. **Automation**: Include notebook execution in scripts/workflows
3. **Consistency**: Standardized execution across team
4. **Integration**: Works with existing modes and tools
5. **CI/CD Ready**: Can be integrated into automated pipelines

## Example Workflow

```powershell
# Complete analysis workflow

# Step 1: Test setup
python main.py --mode test

# Step 2: Run EDA notebooks
python main.py --mode notebooks --notebooks notebooks/00_eda.ipynb notebooks/01_eda.ipynb

# Step 3: Run agent pipeline for structured analysis
python main.py --mode agents --stage all

# Step 4: Run full ML pipeline
python main.py --mode full --no-interactive

# All outputs are now available in artifacts/ and notebook files
```

## Troubleshooting

### "Jupyter not found"
**Solution:** The script auto-installs Jupyter. If it fails:
```powershell
pip install jupyter nbconvert nbformat
```

### "Notebook execution failed"
**Solution:** Check the error message. Common causes:
- Missing dependencies in notebook
- Syntax errors in cells
- File path issues

Fix the issue in the notebook and run again.

### "Timeout expired"
**Solution:** Notebook took >10 minutes to execute. Either:
- Optimize the notebook code
- Run it manually with: `jupyter nbconvert --execute --inplace <notebook>`

### Notebook outputs not saved
**Solution:** Check file permissions. The script needs write access to the notebook files.

## Performance Notes

- **Single notebook**: ~1-5 minutes depending on complexity
- **All notebooks**: ~5-20 minutes total
- **Parallel execution**: Not currently supported (runs sequentially)
- **Memory usage**: Depends on notebook operations

## Future Enhancements

Potential future improvements:
- Parallel notebook execution
- Custom timeout per notebook
- Output to separate files option
- HTML report generation
- Notebook dependency detection

## Summary

The notebook integration provides a seamless way to execute Jupyter notebooks as part of your breast cancer ML pipeline workflow. It's fully integrated with the existing command-line and menu systems, making it easy to run notebooks alongside other analysis modes.

**Key Command:**
```powershell
python main.py --mode notebooks
```

This executes all notebooks and saves outputs in-place, ready for review!
