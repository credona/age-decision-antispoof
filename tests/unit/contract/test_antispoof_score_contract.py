import cv2
import numpy as np
from fastapi.testclient import TestClient

from antispoof.api.main import app

client = TestClient(app)


def _build_jpeg_image_bytes() -> bytes:
    image = np.zeros((80, 80, 3), dtype=np.uint8)

    encoded, buffer = cv2.imencode(".jpg", image)

    assert encoded is True

    return buffer.tobytes()


def test_check_response_exposes_only_public_cred_antispoof_score():
    response = client.post(
        "/check",
        headers={
            "X-Request-ID": "test-request-score",
            "X-Correlation-ID": "test-correlation-score",
        },
        files={"file": ("test.jpg", _build_jpeg_image_bytes(), "image/jpeg")},
    )

    assert response.status_code == 200

    payload = response.json()

    assert "cred_antispoof_score" in payload
    assert 0.0 <= payload["cred_antispoof_score"] <= 1.0

    assert "confidence" not in payload
    assert "spoof_score" not in payload
    assert "threshold" not in payload
    assert "details" not in payload
    assert "cred_score" not in payload
