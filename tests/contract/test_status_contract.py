from fastapi.testclient import TestClient

from antispoof.api.main import app

client = TestClient(app)


def test_health_contract_is_stable_and_privacy_first():
    response = client.get("/health")

    assert response.status_code == 200

    payload = response.json()

    assert set(payload.keys()) == {
        "status",
        "service",
        "version",
        "contract_version",
    }
    assert payload["status"] == "ok"

    assert "confidence" not in payload
    assert "spoof_score" not in payload
    assert "threshold" not in payload
    assert "details" not in payload
    assert "cred_score" not in payload
    assert "raw_score" not in payload
    assert "model_score" not in payload
    assert "heuristic_scores" not in payload


def test_model_status_contract_is_stable_and_uses_model_identifier():
    response = client.get("/engine/status")

    assert response.status_code == 200

    payload = response.json()

    assert set(payload.keys()) == {
        "service",
        "version",
        "contract_version",
        "antispoof_model",
        "heuristics",
    }

    model = payload["antispoof_model"]

    assert "model_id" in model
    assert "model_version" in model
    assert "scoring_policy_id" in model
    assert "path" not in model
    assert "model_path" not in model
    assert "threshold" not in payload
    assert "weights" not in payload
