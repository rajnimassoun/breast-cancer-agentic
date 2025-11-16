import os
import pandas as pd
from agents import privacy


def test_deidentify_drop_and_temp_csv(tmp_path):
    df = pd.DataFrame({
        "name": ["Alice", "Bob"],
        "email": ["a@example.com", "b@example.com"],
        "age": [30, 40],
    })

    # Drop strategy should remove detected identifier columns (name, email)
    out = privacy.deidentify_dataframe(df, strategy="drop")
    assert "age" in out.columns
    # at least one PII column removed
    assert "name" not in out.columns or "email" not in out.columns

    # deidentify_to_temp_csv should write a CSV and return its path
    path = privacy.deidentify_to_temp_csv(df, strategy="drop", cols=None, salt="testsalt")
    assert os.path.exists(path)
    # file should contain same number of rows
    df2 = pd.read_csv(path)
    assert len(df2) == len(df)
    os.remove(path)


def test_deidentify_pseudonymize_deterministic():
    df = pd.DataFrame({"id": ["x1", "x2", "x1"]})
    out1 = privacy.deidentify_dataframe(df, strategy="pseudonymize", cols=["id"], salt="s1")
    out2 = privacy.deidentify_dataframe(df, strategy="pseudonymize", cols=["id"], salt="s1")
    # pseudonymization should be deterministic with same salt
    assert out1["id"].tolist() == out2["id"].tolist()
    # different salt should change pseudonyms
    out3 = privacy.deidentify_dataframe(df, strategy="pseudonymize", cols=["id"], salt="s2")
    assert out3["id"].tolist() != out1["id"].tolist()
