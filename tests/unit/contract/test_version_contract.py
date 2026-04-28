import json
from pathlib import Path

from fastapi.testclient import TestClient

from antispoof.api.main import app

client = TestClient(app)


def test_project_and_compatibility_versions_are_aligned():
    project = json.loads(Path("project.json").read_text(encoding="utf-8"))
    compatibility = json.loads(Path("compatibility.json").read_text(encoding="utf-8"))

    assert compatibility["service"] == project["service_name"]
    assert compatibility["version"] == project["version"]
    assert compatibility["contract_version"] == project["contract_version"]


def test_health_exposes_contract_version():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["contract_version"] == "2.0"


def test_version_endpoint_exposes_project_version():
    response = client.get("/version")

    assert response.status_code == 200
    assert response.json()["version"] == "2.1.0"
    assert response.json()["contract_version"] == "2.0"
