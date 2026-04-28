import json
from pathlib import Path

import cv2
import numpy as np
from fastapi.testclient import TestClient

from antispoof.api.main import app

client = TestClient(app)


def _build_jpeg_image_bytes() -> bytes:
    """Build a valid in-memory JPEG image."""
    image = np.zeros((80, 80, 3), dtype=np.uint8)

    encoded, buffer = cv2.imencode(".jpg", image)

    assert encoded is True

    return buffer.tobytes()


def test_health():
    """Test health endpoint."""
    response = client.get("/health")

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "ok"
    assert payload["service"] == "age-decision-antispoof"
    assert "version" in payload
    project = json.loads(Path("project.json").read_text(encoding="utf-8"))
    assert payload["version"] == project["version"]
    assert payload["contract_version"] == "2.0"


def test_model_status():
    """Test model status endpoint."""
    response = client.get("/model/status")
    payload = response.json()

    assert response.status_code == 200

    assert payload["service"] == "age-decision-antispoof"
    assert "version" in payload
    assert "antispoof_model" in payload
    assert "heuristics" in payload
    assert "threshold" in payload
    assert "weights" in payload

    assert payload["antispoof_model"]["loaded"] is True
    assert payload["antispoof_model"]["type"] == "onnx"
    assert payload["antispoof_model"]["name"] == "MiniFASNetV2"
    assert "path" in payload["antispoof_model"]
    assert payload["antispoof_model"]["exists"] is True
    project = json.loads(Path("project.json").read_text(encoding="utf-8"))
    assert payload["version"] == project["version"]
    assert payload["contract_version"] == "2.0"


def test_check_with_generated_image():
    """Test /check endpoint with an in-memory generated image."""
    response = client.post(
        "/check",
        files={"file": ("test.jpg", _build_jpeg_image_bytes(), "image/jpeg")},
    )

    assert response.status_code == 200

    payload = response.json()

    assert "request_id" in payload
    assert "correlation_id" in payload

    assert payload["request_id"] == payload["correlation_id"]
    assert payload["provider"] == "age-decision-antispoof"

    assert "is_real" in payload
    assert "spoof_detected" in payload
    assert "decision" in payload
    assert "cred_antispoof_score" in payload
    assert 0.0 <= payload["cred_antispoof_score"] <= 1.0
    assert "model_info" in payload
    assert "privacy" in payload

    assert "confidence" not in payload
    assert "spoof_score" not in payload
    assert "threshold" not in payload
    assert "details" not in payload
    assert "cred_score" not in payload

    assert payload["rejection_reason"] is None

    assert payload["privacy"]["privacy_first"] is True
    assert payload["privacy"]["image_persisted"] is False
    assert payload["privacy"]["biometric_template_stored"] is False
    assert payload["privacy"]["raw_image_logged"] is False


def test_check_uses_custom_request_id():
    """Test /check endpoint with a custom request id."""
    response = client.post(
        "/check",
        headers={"X-Request-ID": "test-request-123"},
        files={"file": ("test.jpg", _build_jpeg_image_bytes(), "image/jpeg")},
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["request_id"] == "test-request-123"
    assert payload["correlation_id"] == "test-request-123"


def test_check_uses_custom_request_and_correlation_id():
    """Test /check endpoint with custom request and correlation ids."""
    response = client.post(
        "/check",
        headers={
            "X-Request-ID": "test-request-123",
            "X-Correlation-ID": "test-correlation-456",
        },
        files={"file": ("test.jpg", _build_jpeg_image_bytes(), "image/jpeg")},
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["request_id"] == "test-request-123"
    assert payload["correlation_id"] == "test-correlation-456"


def test_check_rejects_empty_image():
    """Test /check endpoint rejects an empty image payload."""
    response = client.post(
        "/check",
        headers={"X-Request-ID": "test-request-empty"},
        files={"file": ("empty.jpg", b"", "image/jpeg")},
    )

    assert response.status_code == 400

    payload = response.json()

    assert payload == {
        "request_id": "test-request-empty",
        "correlation_id": "test-request-empty",
        "error": {
            "code": "empty_file",
            "message": "Invalid request.",
        },
    }


def test_check_rejects_invalid_image():
    """Test /check endpoint rejects invalid image bytes."""
    response = client.post(
        "/check",
        headers={
            "X-Request-ID": "test-request-invalid",
            "X-Correlation-ID": "test-correlation-invalid",
        },
        files={"file": ("invalid.jpg", b"not-an-image", "image/jpeg")},
    )

    assert response.status_code == 400

    payload = response.json()

    assert payload == {
        "request_id": "test-request-invalid",
        "correlation_id": "test-correlation-invalid",
        "error": {
            "code": "invalid_image",
            "message": "Invalid request.",
        },
    }


def test_benchmark_endpoint_returns_404_when_dataset_is_missing(monkeypatch):
    """Test /benchmark returns 404 when local benchmark dataset is unavailable."""
    from antispoof.api import main

    def fake_run_local_benchmark():
        raise FileNotFoundError("Benchmark labels file not found")

    monkeypatch.setattr(main, "run_local_benchmark", fake_run_local_benchmark)

    response = client.get(
        "/benchmark",
        headers={
            "X-Request-ID": "test-request-benchmark",
            "X-Correlation-ID": "test-correlation-benchmark",
        },
    )

    assert response.status_code == 404

    payload = response.json()

    assert payload == {
        "request_id": "test-request-benchmark",
        "correlation_id": "test-correlation-benchmark",
        "error": {
            "code": "benchmark_dataset_unavailable",
            "message": "Benchmark dataset unavailable.",
        },
    }
