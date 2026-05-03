import json
import logging
import re
from pathlib import Path

import pytest

from antispoof.domain.privacy.safe_logging import (
    assert_privacy_safe_log_text,
    sanitize_log_payload,
    sanitize_log_value,
)

FORBIDDEN_PATTERNS = [
    re.compile(r"data:image/", re.IGNORECASE),
    re.compile(r"base64", re.IGNORECASE),
    re.compile(r"[A-Za-z0-9+/]{120,}={0,2}"),
    re.compile(r"confidence", re.IGNORECASE),
    re.compile(r"threshold", re.IGNORECASE),
    re.compile(r"raw", re.IGNORECASE),
    re.compile(r"payload", re.IGNORECASE),
    re.compile(r"downstream", re.IGNORECASE),
    re.compile(r"spoof_score", re.IGNORECASE),
    re.compile(r"liveness_score", re.IGNORECASE),
    re.compile(r"\.(jpg|jpeg|png|webp|bmp)", re.IGNORECASE),
]


@pytest.mark.parametrize(
    "value",
    [
        b"\xff\xd8\xff\xe0" + b"a" * 512,
        "data:image/png;base64," + ("A" * 256),
        {"image": "A" * 512},
        {"image_base64": "A" * 512},
        {"payload": {"image": "A" * 512}},
        {"confidence": 0.91},
        {"threshold": 0.6},
        {"spoof_score": 0.82},
        {"liveness_score": 0.74},
        {"raw": {"score": 0.98}},
        {"downstream_response": {"confidence": 0.99}},
        {"file_path": "/tmp/selfie.png"},
    ],
)
def test_sanitize_log_value_removes_sensitive_content(value):
    sanitized = sanitize_log_value(value)
    text = json.dumps(sanitized, default=str)

    for pattern in FORBIDDEN_PATTERNS:
        assert not pattern.search(text), text


def test_sanitize_log_payload_keeps_only_public_safe_context():
    payload = {
        "request_id": "req-123",
        "correlation_id": "corr-456",
        "event": "antispoof_check_completed",
        "decision": "uncertain",
        "reason_code": "LOW_SIGNAL",
        "spoof_check_required": True,
        "image": "A" * 512,
        "confidence": 0.88,
        "threshold": 0.6,
        "spoof_score": 0.82,
        "liveness_score": 0.74,
        "raw": {"internal": True},
        "downstream_response": {"confidence": 0.99},
    }

    sanitized = sanitize_log_payload(payload)

    assert sanitized == {
        "request_id": "req-123",
        "correlation_id": "corr-456",
        "event": "antispoof_check_completed",
        "decision": "uncertain",
        "reason_code": "LOW_SIGNAL",
        "spoof_check_required": True,
    }


def test_assert_privacy_safe_log_text_rejects_sensitive_logs():
    unsafe_log = json.dumps(
        {
            "request_id": "req-123",
            "image_base64": "A" * 512,
            "confidence": 0.93,
            "spoof_score": 0.84,
        }
    )

    with pytest.raises(AssertionError):
        assert_privacy_safe_log_text(unsafe_log)


def test_assert_privacy_safe_log_text_accepts_safe_logs():
    safe_log = json.dumps(
        {
            "request_id": "req-123",
            "correlation_id": "corr-456",
            "event": "antispoof_check_completed",
            "decision": "uncertain",
            "reason_code": "LOW_SIGNAL",
            "spoof_check_required": True,
        }
    )

    assert_privacy_safe_log_text(safe_log)


def test_runtime_logs_do_not_expose_sensitive_content(caplog):
    logger = logging.getLogger("age_decision.antispoof.test")

    sensitive_payload = {
        "request_id": "req-123",
        "correlation_id": "corr-456",
        "image": "A" * 512,
        "image_base64": "A" * 512,
        "confidence": 0.96,
        "threshold": 0.6,
        "spoof_score": 0.82,
        "liveness_score": 0.74,
        "raw": {"model_output": [0.1, 0.9]},
        "downstream_response": {"raw": True},
    }

    with caplog.at_level(logging.INFO):
        logger.info(
            "antispoof_event",
            extra={"privacy_safe": sanitize_log_payload(sensitive_payload)},
        )

    rendered_logs = "\n".join(
        f"{record.getMessage()} {record.__dict__}" for record in caplog.records
    )

    assert_privacy_safe_log_text(rendered_logs)


def test_application_source_does_not_log_forbidden_fields_directly():
    app_dir = Path("antispoof")
    assert app_dir.exists(), "antispoof directory is missing"

    forbidden_tokens = [
        "confidence",
        "threshold",
        "image_base64",
        "base64",
        "downstream_response",
        "raw_response",
        "raw_payload",
        "spoof_score",
        "liveness_score",
    ]

    violations = []

    for path in app_dir.rglob("*.py"):
        if path.name == "safe_logging.py":
            continue

        text = path.read_text(encoding="utf-8")

        for line_no, line in enumerate(text.splitlines(), start=1):
            normalized = line.lower()

            if "log" not in normalized and "logger" not in normalized:
                continue

            for token in forbidden_tokens:
                if token in normalized:
                    violations.append(f"{path}:{line_no}: {line.strip()}")

    assert not violations, "Forbidden logging usage found:\n" + "\n".join(violations)
