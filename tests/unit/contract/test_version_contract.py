import json
from pathlib import Path

from fastapi.testclient import TestClient

from antispoof.api.main import app

client = TestClient(app)


def test_version_endpoint_exists_in_openapi():
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert "/version" in response.json()["paths"]


def test_version_endpoint_returns_public_metadata():
    response = client.get("/version")
    body = response.json()

    assert response.status_code == 200
    assert set(body.keys()) == {
        "service_name",
        "app_name",
        "version",
        "contract_version",
        "repository",
        "image",
    }


def test_version_endpoint_exposes_project_version():
    project = json.loads(Path("project.json").read_text(encoding="utf-8"))

    response = client.get("/version")

    assert response.status_code == 200
    assert response.json()["version"] == project["version"]
