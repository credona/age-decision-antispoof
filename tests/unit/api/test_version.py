import json
from pathlib import Path

from fastapi.testclient import TestClient

from antispoof.api.main import app

client = TestClient(app)


def test_version_returns_project_metadata():
    project = json.loads(Path("project.json").read_text(encoding="utf-8"))

    response = client.get("/version")

    assert response.status_code == 200
    assert response.json() == {
        "service_name": project["service_name"],
        "app_name": project["app_name"],
        "version": project["version"],
        "contract_version": project["contract_version"],
        "repository": project["repository"],
        "image": project["image"],
    }
