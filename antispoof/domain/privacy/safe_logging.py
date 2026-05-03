import re
from collections.abc import Mapping, Sequence
from typing import Any

PUBLIC_LOG_KEYS = {
    "request_id",
    "correlation_id",
    "event",
    "decision",
    "is_live",
    "reason_code",
    "reason_codes",
    "spoof_check_required",
    "error_code",
}

FORBIDDEN_LOG_KEY_PARTS = (
    "image",
    "base64",
    "payload",
    "raw",
    "score",
    "confidence",
    "threshold",
    "downstream",
    "file",
    "path",
)

FORBIDDEN_LOG_PATTERNS = (
    re.compile(r"data:image/", re.IGNORECASE),
    re.compile(r"base64", re.IGNORECASE),
    re.compile(r"[A-Za-z0-9+/]{120,}={0,2}"),
    re.compile(r"confidence", re.IGNORECASE),
    re.compile(r"threshold", re.IGNORECASE),
    re.compile(r"\braw\b", re.IGNORECASE),
    re.compile(r"payload", re.IGNORECASE),
    re.compile(r"downstream", re.IGNORECASE),
    re.compile(r"spoof_score", re.IGNORECASE),
    re.compile(r"liveness_score", re.IGNORECASE),
    re.compile(r"\.(jpg|jpeg|png|webp|bmp)", re.IGNORECASE),
)


def sanitize_log_value(value: Any) -> Any:
    if isinstance(value, bytes | bytearray | memoryview):
        return "[REDACTED]"

    if isinstance(value, str):
        if _is_sensitive_text(value):
            return "[REDACTED]"
        return value

    if isinstance(value, Mapping):
        return {
            key: sanitize_log_value(item)
            for key, item in value.items()
            if not _is_sensitive_key(str(key))
        }

    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        return [sanitize_log_value(item) for item in value]

    return value


def sanitize_log_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: sanitize_log_value(value)
        for key, value in payload.items()
        if key in PUBLIC_LOG_KEYS and not _is_sensitive_key(key)
    }


def assert_privacy_safe_log_text(text: str) -> None:
    for pattern in FORBIDDEN_LOG_PATTERNS:
        assert not pattern.search(text), f"Unsafe log content detected: {pattern.pattern}"


def _is_sensitive_key(key: str) -> bool:
    normalized = key.lower()
    return any(part in normalized for part in FORBIDDEN_LOG_KEY_PARTS)


def _is_sensitive_text(value: str) -> bool:
    return any(pattern.search(value) for pattern in FORBIDDEN_LOG_PATTERNS)
