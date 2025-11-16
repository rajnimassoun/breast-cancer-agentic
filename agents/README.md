Agent Interface — guidelines for implementing `eda_agent.py` and `fe_agent.py`

Purpose
- Provide a small, stable contract so multiple contributors can implement agents
  that the notebook's adapter can load and run reliably.

Files
- `agents/eda_agent.py` should expose a callable `run_eda_report`.
- `agents/fe_agent.py` should expose `propose_features` and `apply_features`.

`run_eda_report` contract
- Signature: should accept at least one of these calling styles:
  - `run_eda_report(df=DataFrame, target_col=..., out_dir=...)`
  - `run_eda_report(dataset_path=str, target_col=..., out_dir=...)`
- Behavior:
  - Write any artifacts (reports, csvs, plots) into `out_dir` (do not assume cwd).
  - Return a JSON-serializable dict with at least `out_dir` and/or `summary_path`.
  - Prefer not to rely on global state.
- Example return value:
  ```json
  {"out_dir": "artifacts/eda/agent_xyz", "summary_path": "artifacts/eda/agent_xyz/report.html"}
  ```

`propose_features` / `apply_features` contract
- `propose_features(X, y=None, max_interactions=20) -> List[Dict]`
  - Return a list of proposal dicts describing candidate feature transformations.
- `apply_features(X, proposals, dry_run=False) -> (X_new, metadata)`
  - If `dry_run=True`, do not persist changes; return transformed data + metadata.
  - Metadata should include `{"applied": [...], "count": N}`.

Safety and logging
- Avoid executing arbitrary shell commands or network calls without clear intent.
- Write logs and stdout to `out_dir` so the notebook can capture and persist them.

Testing locally
- Use the `example_run_eda_report` in `agents/agent_interface.py` as a starting point.
- The notebook's adapter will try (in order): package import, file-path import, then fall back
  to safe stubs. Keep this in mind when testing in development vs packaged installs.

Notes for integrators
- The notebook uses a subprocess-based runner by default for safety and timeouts.
  Returning JSON-serializable results makes parsing from the runner robust.
- If you need additional runtime arguments, accept `**kwargs` in your functions so
  the adapter can pass extras without breaking compatibility.
