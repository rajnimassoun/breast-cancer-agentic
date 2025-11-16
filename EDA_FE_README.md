# Breast Cancer Agentic: EDA & Feature Engineering

## Overview
This notebook implements a **safe, auditable, and modular** approach to exploratory data analysis (EDA) and feature engineering for the breast cancer classification task. The design prioritizes:
- **Safety**: Subprocess sandboxing with timeouts, de-identification before agent runs
- **Auditability**: Structured JSONL logging of all agent operations
- **Modularity**: Agents can be developed independently and swapped at runtime
- **Reproducibility**: Fixed random states, versioned transformers, explicit configuration

## Setup

### 1. Install Dependencies
```bash
# From repo root
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # Windows
# or: source .venv/bin/activate  # Unix

pip install -r requirements-dev.txt
```

### 2. Run the Notebook
#### Interactive (Recommended for Development)
```bash
jupyter notebook notebooks/00_eda.ipynb
# Run cells top-to-bottom; can adjust DEID_STRATEGY and CONFIRM_APPLY as needed
```

#### Non-Interactive (CI/Automation)
```bash
jupyter nbconvert --to notebook --execute notebooks/00_eda.ipynb \
  --output 00_eda.executed.ipynb \
  --ExecutePreprocessor.timeout=600
```

## Architecture

### Notebook Structure
1. **Imports & Config**: Load libraries and set random seed
2. **Repository Root & Paths**: Detect project root and set up artifact directories
3. **Load Dataset**: Read breast cancer CSV and split into X, y
4. **EDA Cells**: Correlation heatmap, target distribution, KDE plots, numeric overview
5. **Agent Loader & Safe Adapter**: Load agents with resilient fallback to stubs
6. **Feature Engineering**: Ratio features, outlier capping, scaling
7. **Mutual Information**: Feature ranking by correlation with target
8. **Train/Test Split**: Stratified split for fair model evaluation
9. **XGBoost + GridSearchCV**: Hyperparameter tuning and final model

### Key Global Configuration (Set Before Running Cells)
```python
# De-identification strategy: 'drop', 'pseudonymize', or 'generalize'
DEID_STRATEGY = 'drop'

# Specific columns to de-identify (None = auto-detect)
DEID_COLS = None

# Salt for pseudonymization (rotate regularly in production)
DEID_SALT = 'agentic-default-salt'

# Allow apply_features to persist changes without prompt
CONFIRM_APPLY = False

# Alternative dataset path (if None, uses in-memory df)
DATA_PATH = None
```

## Safety Features

### 1. De-Identification (Privacy)
Before subprocess agents receive data, the notebook de-identifies the dataframe:
- **drop**: removes detected identifier columns (name, email, id, etc.)
- **pseudonymize**: replaces values with salted hashes
- **generalize**: coarsens numeric values (age ranges, quantiles)

Audit log records every de-identification event with strategy and column details.

### 2. Subprocess Sandboxing
Agents run in separate processes via `subprocess.run()`:
- Timeouts via the OS (cannot be bypassed like thread timeouts)
- stdout/stderr captured to `artifacts/eda/agent_stdout_*.log` and `agent_stderr_*.log`
- Audit record for each subprocess completion with artifact paths
- Fallback to in-process execution if subprocess unavailable

### 3. Structured Audit Logging
All agent operations write newline-delimited JSON to `artifacts/eda/audit_log.jsonl`:
```json
{"event_type": "eda_run", "actor": "notebook", "action": "run_eda", "timestamp": "2025-11-15T12:34:56.789Z", "duration_seconds": 2.3, "success": true}
{"event_type": "deidentify", "actor": "notebook", "action": "deidentify_to_temp_csv", "timestamp": "2025-11-15T12:34:56.800Z", "details": {"strategy": "drop", "cols": null}}
```

### 4. Dry-Run & Confirmation for Destructive Ops
The `apply_features()` function:
- Defaults to `dry_run=True` (no persistence, safe to test)
- If `dry_run=False`, requires one of:
  1. `confirm=True` argument
  2. `CONFIRM_APPLY=True` global in notebook
  3. Interactive prompt (type 'yes' to confirm)

This prevents accidental data loss in automated workflows.

## Output Artifacts

### Data
- `data/engineered/breast_cancer_engineered.csv`: Scaled, clipped features + target
- `artifacts/engineering/transformers.pkl`: StandardScaler + feature metadata

### Logs & Analysis
- `artifacts/eda/audit_log.jsonl`: Structured audit events (de-id, subprocess, agent ops)
- `artifacts/eda/agent_adapter_*.log`: Console + file logs (timestamps in filename)
- `artifacts/eda/agent_stdout_*.log` / `agent_stderr_*.log`: Agent subprocess output
- `artifacts/eda/mutual_info_ranking.csv`: Feature ranks by mutual information

## Agent Interface

### EDA Agent (`agents/eda_agent.py`)
```python
def run_eda_report(df=None, dataset_path=None, target_col=None, out_dir=None) -> dict:
    """
    Perform exploratory data analysis.
    
    Args:
        df: pandas DataFrame (if provided, dataset_path is ignored)
        dataset_path: path to CSV file (used if df is None)
        target_col: name of target column
        out_dir: directory to save plots/summaries
    
    Returns:
        dict with keys: summary_path, plots, stats, etc.
    """
```

### Feature Engineering Agent (`agents/fe_agent.py`)
```python
def propose_features(X, y=None, max_interactions=20) -> list:
    """Generate feature engineering proposals (list of dicts)."""

def apply_features(X, proposals, dry_run=True, confirm=False) -> tuple:
    """Apply proposals to X; return (X_new, metadata)."""
```

See `agents/agent_interface.py` for full protocol definitions.

## Testing

### Run Unit Tests
```bash
pytest -q agents/tests/test_privacy.py agents/tests/test_audit.py
```

### Validate De-Identification
```python
# In notebook or script
from agents.privacy import deidentify_dataframe
df_deid = deidentify_dataframe(df, strategy='drop')
print(f"Original columns: {df.columns.tolist()}")
print(f"After de-id: {df_deid.columns.tolist()}")
```

### Validate Audit Logging
```python
# In notebook
import json
with open('artifacts/eda/audit_log.jsonl', 'r') as f:
    records = [json.loads(line) for line in f if line.strip()]
print(f"Total audit events: {len(records)}")
for r in records[:3]:
    print(f"  {r['event_type']}: {r['action']}")
```

## Handoff to Modeling Team

1. **Engineered Data**: `data/engineered/breast_cancer_engineered.csv`
   - All features scaled (StandardScaler), clipped at percentiles
   - Target column appended
   - Ready for direct model input

2. **Transformer Artifacts**: `artifacts/engineering/transformers.pkl`
   - Contains scaler and metadata
   - Use for test/production transforms

3. **Feature Metadata**: `artifacts/eda/mutual_info_ranking.csv`
   - Feature importance ranking
   - Can be used for feature selection in modeling

4. **Audit Trail**: `artifacts/eda/audit_log.jsonl`
   - Full traceability of EDA ops
   - Timestamps, success/failure status, de-identification records
   - Can be used for compliance reporting

## Customization

### To Add Custom EDA Agent
1. Create `agents/my_eda_agent.py` with a `run_eda_report(...)` function
2. In notebook, update the import strategy to load from that file
3. Optionally wrap with `audit_event()` context manager for logging

### To Use Real Data Path
```python
# In notebook, before running Agent Loader cell:
DATA_PATH = r"C:\path\to\preprocessed_data.csv"
```

### To Skip De-Identification (Not Recommended)
```python
DEID_STRATEGY = 'drop'
DEID_COLS = []  # empty list = no columns de-identified
```

## Production Considerations

- **Audit Log Rotation**: Implement rotation/archival for `audit_log.jsonl` in high-volume environments
- **Salt Management**: Store `DEID_SALT` in a secrets manager; rotate periodically
- **PII Detection**: Current heuristics detect common column names; add NER for free-text fields
- **Multi-Process Audit**: For parallel agent execution, use a centralized log collector (syslog/HTTP)
- **Container Sandboxing**: Run agents in Docker/Singularity for additional isolation
