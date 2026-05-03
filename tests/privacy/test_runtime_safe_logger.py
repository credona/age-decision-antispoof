import json
import logging

from antispoof.infrastructure.logging.safe_logger import log_event


def test_runtime_safe_logger_filters_sensitive_payload(caplog):
    logger = logging.getLogger("antispoof")
    logger.propagate = True

    with caplog.at_level(logging.INFO, logger="antispoof"):
        log_event(
            "antispoof_check_completed",
            {
                "request_id": "req-1",
                "correlation_id": "corr-1",
                "decision": "real",
                "cred_antispoof_score": 0.91,
                "threshold": 0.5,
                "raw_scores": [0.1, 0.8, 0.1],
                "image_base64": "A" * 512,
                "provider": "age-decision-antispoof",
                "error_code": "invalid_image",
            },
        )

    logger.propagate = False

    payload = json.loads(caplog.records[-1].message)

    assert payload["event"] == "antispoof_check_completed"
    assert payload["request_id"] == "req-1"
    assert payload["correlation_id"] == "corr-1"
    assert payload["decision"] == "real"
    assert payload["error_code"] == "invalid_image"

    assert "cred_antispoof_score" not in payload
    assert "threshold" not in payload
    assert "raw_scores" not in payload
    assert "image_base64" not in payload
    assert "provider" not in payload
