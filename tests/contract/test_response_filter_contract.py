from antispoof.api.response_filter import filter_check_response


def test_check_response_filter_ignores_internal_fields():
    payload = filter_check_response(
        {
            "request_id": "req-1",
            "correlation_id": "corr-1",
            "provider": "age-decision-antispoof",
            "decision": "real",
            "is_real": True,
            "spoof_detected": False,
            "cred_antispoof_score": 0.91,
            "rejection_reason": None,
            "privacy": {
                "image_persisted": False,
                "raw_image_logged": False,
                "biometric_template_stored": False,
                "processing": "ephemeral",
            },
            "model_info": {
                "antispoof_model": "MiniFASNetV2",
                "model_type": "onnx",
                "heuristics": ["texture", "screen_pattern", "blur"],
            },
            "confidence": 0.99,
            "model_score": 0.95,
            "spoof_score": 0.05,
            "raw_scores": [0.01, 0.98, 0.01],
            "details": {"internal": True},
            "threshold": 0.5,
        }
    )

    assert "confidence" not in payload
    assert "model_score" not in payload
    assert "spoof_score" not in payload
    assert "raw_scores" not in payload
    assert "details" not in payload
    assert "threshold" not in payload
