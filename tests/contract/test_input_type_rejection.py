from fastapi.testclient import TestClient

from antispoof.api.main import app

client = TestClient(app)


def test_reject_image_sequence():
    response = client.post(
        "/check?input_type=image_sequence",
        files={"file": ("frame.png", b"fake-image", "image/png")},
    )

    assert response.status_code == 400

    body = response.json()

    assert body["error"]["code"] == "UNSUPPORTED_INPUT_TYPE"
    assert "image_sequence" in body["error"]["message"]

    _assert_no_sensitive_fields(body)


def test_reject_video():
    response = client.post(
        "/check?input_type=video",
        files={"file": ("video.mp4", b"fake-video", "video/mp4")},
    )

    assert response.status_code == 400

    body = response.json()

    assert body["error"]["code"] == "UNSUPPORTED_INPUT_TYPE"
    assert "video" in body["error"]["message"]

    _assert_no_sensitive_fields(body)


def _assert_no_sensitive_fields(body: dict):
    text = str(body).lower()

    forbidden = [
        "confidence",
        "threshold",
        "raw",
        "score",
        "downstream",
        "spoof_score",
        "liveness_score",
    ]

    for field in forbidden:
        assert field not in text
