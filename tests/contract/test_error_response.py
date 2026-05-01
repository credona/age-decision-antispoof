from io import BytesIO

from fastapi.testclient import TestClient

from antispoof.api.main import app

client = TestClient(app)


def test_check_invalid_image_returns_stable_error_response():
    response = client.post(
        "/check",
        headers={
            "X-Request-ID": "test-request-invalid-image",
            "X-Correlation-ID": "test-correlation-invalid-image",
        },
        files={
            "file": ("invalid.jpg", BytesIO(b"not-a-valid-image"), "image/jpeg"),
        },
    )

    assert response.status_code == 400

    payload = response.json()

    assert set(payload.keys()) == {"request_id", "correlation_id", "error"}
    assert set(payload["error"].keys()) == {"code", "message"}
    assert payload["request_id"] == "test-request-invalid-image"
    assert payload["correlation_id"] == "test-correlation-invalid-image"
    assert payload["error"]["code"] == "invalid_image"
    assert payload["error"]["message"] == "Invalid request."


def test_check_empty_file_returns_stable_error_response():
    response = client.post(
        "/check",
        headers={
            "X-Request-ID": "test-request-empty-file",
            "X-Correlation-ID": "test-correlation-empty-file",
        },
        files={
            "file": ("empty.jpg", BytesIO(b""), "image/jpeg"),
        },
    )

    assert response.status_code == 400

    payload = response.json()

    assert set(payload.keys()) == {"request_id", "correlation_id", "error"}
    assert set(payload["error"].keys()) == {"code", "message"}
    assert payload["request_id"] == "test-request-empty-file"
    assert payload["correlation_id"] == "test-correlation-empty-file"
    assert payload["error"]["code"] == "empty_file"
    assert payload["error"]["message"] == "Invalid request."


def test_check_missing_file_returns_stable_validation_error_shape():
    response = client.post(
        "/check",
        headers={
            "X-Request-ID": "test-request-missing-file",
            "X-Correlation-ID": "test-correlation-missing-file",
        },
    )

    assert response.status_code == 400

    payload = response.json()

    assert set(payload.keys()) == {"request_id", "correlation_id", "error"}
    assert set(payload["error"].keys()) == {"code", "message"}
    assert payload["request_id"] == "test-request-missing-file"
    assert payload["correlation_id"] == "test-correlation-missing-file"
    assert payload["error"]["code"] == "missing_file"
    assert payload["error"]["message"] == "Invalid request."


def test_check_missing_file_falls_back_to_request_id_as_correlation_id():
    response = client.post(
        "/check",
        headers={
            "X-Request-ID": "test-request-missing-file-alt",
        },
    )

    assert response.status_code == 400

    payload = response.json()

    assert set(payload.keys()) == {"request_id", "correlation_id", "error"}
    assert payload["request_id"] == "test-request-missing-file-alt"
    assert payload["correlation_id"] == "test-request-missing-file-alt"
    assert payload["error"]["code"] == "missing_file"
    assert payload["error"]["message"] == "Invalid request."
