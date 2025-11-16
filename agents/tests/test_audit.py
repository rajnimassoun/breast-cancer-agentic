import json
import tempfile
from agents.audit_logger import get_default_audit


def test_audit_event_writes_start_finish(tmp_path):
    artifacts_dir = tmp_path
    audit = get_default_audit(artifacts_dir=artifacts_dir)
    # The audit returns an object with .filepath
    assert audit.filepath is not None

    with audit.audit_event(event_type="test_event", actor="pytest", action="run_test", target="unit_test"):
        # inside the context we do nothing; the context manager should log start and finish
        pass

    # Read the JSONL audit file and ensure it contains at least two records
    with open(audit.filepath, "r", encoding="utf-8") as fh:
        lines = [line.strip() for line in fh if line.strip()]

    assert len(lines) >= 2
    objs = [json.loads(l) for l in lines]
    types = [o.get("event_type") for o in objs]
    assert "test_event" in types
