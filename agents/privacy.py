"""Privacy / de-identification helpers.

Provide simple, auditable de-identification utilities suitable for notebooks
and local agents. This module focuses on basic, well-understood strategies:
- drop: remove obvious identifier columns
- pseudonymize: replace identifiers with salted SHA256 hashes
- generalize: coarse-grain numeric/date fields

These are NOT a substitute for a formal privacy review; choose strategies
appropriate to your data governance and legal requirements.
"""
from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

import pandas as pd


_COMMON_ID_KEYWORDS = ["name", "email", "id", "ssn", "phone", "dob", "date_of_birth"]


def _detect_identifier_columns(df: pd.DataFrame) -> List[str]:
    # Heuristic detection of likely identifier columns. This is intentionally
    # simple — projects with stricter requirements should supply explicit
    # `cols` to `deidentify_dataframe` or provide an enterprise-grade PII scanner.
    cols = []
    for c in df.columns:
        low = str(c).lower()
        for k in _COMMON_ID_KEYWORDS:
            if k in low:
                cols.append(c)
                break
    return cols


def pseudonymize_series(s: pd.Series, salt: str) -> pd.Series:
    def _hash(v: object) -> str:
        if pd.isna(v):
            return ""
        h = hashlib.sha256((salt + str(v)).encode("utf-8")).hexdigest()
        return h
    return s.map(_hash)


def deidentify_dataframe(df: pd.DataFrame,
                         strategy: str = "drop",
                         cols: Optional[Iterable[str]] = None,
                         salt: str = "agentic-default-salt") -> Tuple[pd.DataFrame, dict]:
    """Return a de-identified copy of `df` plus metadata about actions taken.

    Args:
        df: source DataFrame
        strategy: one of 'drop', 'pseudonymize', 'generalize'
        cols: optional list of columns to consider; if None, auto-detect common ids
        salt: salt used for pseudonymization

    Returns: (df_deid, metadata)
    """
    # Work on a copy to avoid surprising callers by mutating their DataFrame
    df2 = df.copy()
    cols_list = list(cols) if cols is not None else _detect_identifier_columns(df2)
    metadata = {
        "strategy": strategy,
        "cols_targeted": cols_list,
    }

    if strategy == "drop":
        # Irreversible removal: drop the identified columns entirely.
        # Use this when you do NOT need to re-link records later.
        df2 = df2.drop(columns=cols_list, errors="ignore")
        metadata["action"] = "dropped_columns"
        return df2, metadata

    if strategy == "pseudonymize":
        # Replace sensitive values with salted hashes. This is reversible only
        # if you keep the original mapping (not performed here). Treat the
        # salt as a secret; store it securely if you intend to re-link data.
        for c in cols_list:
            new_name = f"{c}_pseudonym"
            df2[new_name] = pseudonymize_series(df2[c], salt)
        # Remove original columns to avoid accidental leakage
        df2 = df2.drop(columns=cols_list, errors="ignore")
        metadata["action"] = "pseudonymized"
        return df2, metadata

    if strategy == "generalize":
        # Coarsen selected columns to reduce identifiability while keeping
        # signal useful for modeling. This strategy is lossy but may preserve
        # more analytical utility than a full drop.
        for c in cols_list:
            ser = df2[c]
            if pd.api.types.is_datetime64_any_dtype(ser):
                df2[c] = ser.dt.year
            elif pd.api.types.is_numeric_dtype(ser):
                df2[c] = ser.round(2)
            else:
                # Truncate long strings to reduce risk from free text
                df2[c] = ser.astype(str).str[:32]
        metadata["action"] = "generalized"
        return df2, metadata

    raise ValueError(f"Unknown de-identification strategy: {strategy}")


def deidentify_to_temp_csv(df: pd.DataFrame,
                           strategy: str = "drop",
                           cols: Optional[Iterable[str]] = None,
                           salt: str = "agentic-default-salt") -> str:
    """Apply de-identification and write the result to a temporary CSV.

    Returns the path to the temporary CSV file (caller should unlink when done).
    """
    # Produce the de-identified DataFrame and write to a temp CSV for the
    # subprocess agent to consume. Caller is responsible for removing the file.
    df_deid, metadata = deidentify_dataframe(df, strategy=strategy, cols=cols, salt=salt)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w", encoding="utf-8")
    df_deid.to_csv(tmp.name, index=False)
    tmp.close()
    return tmp.name


__all__ = ["deidentify_dataframe", "deidentify_to_temp_csv", "pseudonymize_series"]
