import json
from pathlib import Path


def test_project_runtime_uses_common_configuration_without_dev_prod_duplication():
    project = json.loads(Path("project.json").read_text(encoding="utf-8"))

    runtime = project["runtime"]

    assert "common" in runtime
    assert runtime["dev"] == {}
    assert runtime["prod"] == {}


def test_project_runtime_uses_model_identifier_not_model_path():
    project = json.loads(Path("project.json").read_text(encoding="utf-8"))

    runtime_common = project["runtime"]["common"]

    assert "ANTISPOOF_MODEL_ID" in runtime_common
    assert "MODEL_PATH" not in runtime_common
    assert "ANTISPOOF_MODEL_PATH" not in runtime_common


def test_project_runtime_does_not_expose_scoring_policy_as_runtime_config():
    project = json.loads(Path("project.json").read_text(encoding="utf-8"))

    runtime_text = json.dumps(project["runtime"])

    assert "SPOOF_THRESHOLD" not in runtime_text
    assert "ANTISPOOF_THRESHOLD" not in runtime_text
    assert "MODEL_WEIGHT" not in runtime_text
    assert "TEXTURE_WEIGHT" not in runtime_text
    assert "SCREEN_WEIGHT" not in runtime_text
