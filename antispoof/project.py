import json
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel


class ProjectMetadata(BaseModel):
    service_name: str
    app_name: str
    version: str
    contract_version: str
    repository: str
    image: str


@lru_cache
def get_project_metadata() -> ProjectMetadata:
    project_file = Path(__file__).resolve().parent.parent / "project.json"

    with project_file.open(encoding="utf-8") as file:
        return ProjectMetadata.model_validate(json.load(file))


project_metadata = get_project_metadata()
