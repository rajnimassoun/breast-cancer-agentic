"""Audit & compliance logging helpers for agentic notebook and agents.

This module provides a simple, thread-safe JSONL audit logger plus a
context manager and decorator to record start/finish/failure events with
timestamps, duration, and optional structured details. Designed for easy
integration into the notebook adapter and agent entrypoints.

Usage (simple):
    from agents.audit_logger import get_default_audit, audit_event
    audit = get_default_audit(artifacts_dir=ARTIFACTS_EDA)
    with audit.audit_event(event_type='eda_run', actor='notebook', action='run_eda'):
        # call run_eda_with_timeout(...) or other agent functions

The logger writes newline-delimited JSON records to `audit_log.jsonl`
under the provided artifacts directory.
"""
from __future__ import annotations

import json
import threading
import uuid
from contextlib import ContextDecorator
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
import logging

_LOGGER = logging.getLogger(__name__)


@dataclass
class AuditRecord:
    event_id: str
    event_type: str
    actor: Optional[str]
    action: Optional[str]
    target: Optional[str]
    timestamp: str
    duration_seconds: Optional[float] = None
    success: Optional[bool] = None
    details: Dict[str, Any] = field(default_factory=dict)


class AuditLogger:
    """Thread-safe JSONL audit logger.

    The logger appends JSON records to `audit_log.jsonl`. Multiple processes
    writing to the same file are not synchronized by this class; use a
    log-collector for multi-process setups (or configure a central audit
    service).
    """

    def __init__(self, artifacts_dir: Optional[Path] = None, filename: str = "audit_log.jsonl"):
        self.artifacts_dir = Path(artifacts_dir) if artifacts_dir else Path.cwd() / "artifacts" / "eda"
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        self.filepath = self.artifacts_dir / filename
        self._lock = threading.Lock()

    def _now_iso(self) -> str:
        return datetime.utcnow().isoformat() + "Z"

    def log(self,
            event_type: str,
            actor: Optional[str] = None,
            action: Optional[str] = None,
            target: Optional[str] = None,
            details: Optional[Dict[str, Any]] = None,
            success: Optional[bool] = None,
            duration_seconds: Optional[float] = None) -> AuditRecord:
        # Build the audit record dataclass instance. Use UUID for traceability
        rec = AuditRecord(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            actor=actor,
            action=action,
            target=target,
            timestamp=self._now_iso(),
            duration_seconds=duration_seconds,
            success=success,
            details=details or {},
        )

        # Serialize to JSONL and append under a lock to ensure thread-safety
        # (note: this does not provide cross-process atomicity; use a central
        # collector or rotate logs via external tooling in multi-process setups)
        line = json.dumps(asdict(rec), default=str, ensure_ascii=False)
        with self._lock:
            with open(self.filepath, "a", encoding="utf-8") as fh:
                fh.write(line + "\n")

        # Also emit a concise info-level log so operators see audit events in stdout
        _LOGGER.info("AUDIT %s action=%s target=%s id=%s", rec.event_type, rec.action, rec.target, rec.event_id)
        return rec

    def audit_event(self, event_type: str, actor: Optional[str] = None, action: Optional[str] = None,
                    target: Optional[str] = None, details: Optional[Dict[str, Any]] = None) -> "AuditEvent":
        """Create a context manager that logs start/end/failure for an event.

        Example:
            with audit.audit_event('apply_features', actor='notebook', action='apply'):
                apply_features(...)
        """
        return AuditEvent(self, event_type=event_type, actor=actor, action=action, target=target, details=details)


class AuditEvent(ContextDecorator):
    """Context manager & decorator for auditing a scoped operation.

    On entry it logs an initial record (start). On exit it logs a completion
    record with duration and success/failure state and exception details when
    applicable.
    """

    def __init__(self, logger: AuditLogger, *, event_type: str, actor: Optional[str] = None,
                 action: Optional[str] = None, target: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        self.logger = logger
        self.event_type = event_type
        self.actor = actor
        self.action = action
        self.target = target
        self.details = details or {}
        self._start = None
        self._start_record = None

    def __enter__(self):
        self._start = datetime.utcnow()
        self._start_record = self.logger.log(
            event_type=self.event_type,
            actor=self.actor,
            action=self.action,
            target=self.target,
            # mark this record as the start phase
            details={**(self.details or {}), "phase": "start"},
            success=None,
            duration_seconds=None,
        )
        return self

    def __exit__(self, exc_type, exc, tb):
        end = datetime.utcnow()
        duration = (end - self._start).total_seconds() if self._start else None
        success = exc is None
        extra_details = dict(self.details or {})
        if exc is not None:
            # Keep exception string and type for forensic purposes
            # Capture exception info for later auditing/forensics. Avoid storing
            # full tracebacks in the JSONL to reduce noise; the adapter already
            # writes stderr/tracebacks to separate logs.
            extra_details.update({"error_type": str(exc_type), "error": str(exc)})

        self.logger.log(
            event_type=self.event_type,
            actor=self.actor,
            action=self.action,
            target=self.target,
            # mark the completion/end phase and include duration and success
            details={**extra_details, "phase": "end"},
            success=success,
            duration_seconds=duration,
        )

        # Do not suppress exceptions
        return False


# Convenience singleton factory for quick usage in notebooks and agents
_DEFAULT_AUDIT: Optional[AuditLogger] = None


def get_default_audit(artifacts_dir: Optional[Path] = None) -> AuditLogger:
    """Return a process-global AuditLogger instance (lazy)."""
    global _DEFAULT_AUDIT
    if _DEFAULT_AUDIT is None:
        _DEFAULT_AUDIT = AuditLogger(artifacts_dir=artifacts_dir)
    return _DEFAULT_AUDIT


def audit_decorator(event_type: str, actor: Optional[str] = None, action: Optional[str] = None, target: Optional[str] = None):
    """Decorator to wrap callables and emit audit start/end records.

    The decorated function will have its start and end logged to the
    default audit logger. Exceptions are logged as failures and re-raised.
    """
    def _decorator(fn):
        def _wrapped(*args, **kwargs):
            audit = get_default_audit()
            with audit.audit_event(event_type=event_type, actor=actor, action=action, target=target,
                                   details={"fn": getattr(fn, "__name__", str(fn))}):
                return fn(*args, **kwargs)
        _wrapped.__name__ = getattr(fn, "__name__", "wrapped")
        return _wrapped
    return _decorator


__all__ = ["AuditLogger", "get_default_audit", "audit_decorator", "AuditEvent"]
