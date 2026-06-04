from antispoof.api.response_filter import filter_check_response

FORBIDDEN_CALIBRATION_FIELDS = (
    "calibration_parameters",
    "final_score_offset",
    "final_score_floor",
    "final_score_ceiling",
    "cred_antispoof_score_offset",
    "cred_antispoof_score_floor",
    "cred_antispoof_score_ceiling",
    "private_payload",
    "thresholds",
    "weights",
    "margins",
    "calibration_internals",
    "signature",
    "payload_hash",
    "policy_id",
)


def test_response_filter_strips_runtime_calibration_private_fields() -> None:
    payload = {
        "request_id": "req-test",
        "correlation_id": "corr-test",
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
        "engine_info": {
            "antispoof_model": "MiniFASNetV2",
            "model_type": "onnx",
            "heuristics": ["texture", "screen_pattern", "blur"],
        },
        "private_payload": {
            "calibration_parameters": {
                "final_score_offset": 0.1,
                "weights": {"private": 0.4},
                "margins": {"private": 2},
            }
        },
        "calibration_internals": {
            "thresholds": [0.5],
            "weights": [0.4],
            "margins": [2],
        },
        "policy_id": "antispoof-private-policy",
        "signature": "private-signature",
        "payload_hash": "sha256:private",
    }

    filtered = filter_check_response(payload)
    serialized = str(filtered)

    for forbidden in FORBIDDEN_CALIBRATION_FIELDS:
        assert forbidden not in serialized


def test_pipeline_result_does_not_expose_runtime_calibration_internals() -> None:
    from antispoof import AntiSpoofPipeline

    pipeline = AntiSpoofPipeline()

    assert "calibration" not in pipeline.predict_from_path("test-face.jpg").details
    assert "weights" not in pipeline.predict_from_path("test-face.jpg").details
