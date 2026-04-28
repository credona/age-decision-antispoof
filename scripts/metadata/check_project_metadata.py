import json
import re
from pathlib import Path

PROJECT_FILE = Path("project.json")
CHANGELOG_FILE = Path("CHANGELOG.md")
README_FILE = Path("README.md")


def main() -> None:
    metadata = json.loads(PROJECT_FILE.read_text(encoding="utf-8"))

    required_fields = [
        "service_name",
        "app_name",
        "version",
        "contract_version",
        "repository",
        "image",
    ]

    for field in required_fields:
        if not metadata.get(field):
            raise SystemExit(f"Missing project metadata field: {field}")

    version = metadata["version"]

    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise SystemExit(f"Invalid semantic version: {version}")

    changelog = CHANGELOG_FILE.read_text(encoding="utf-8")
    if f"<h2>{version}</h2>" not in changelog:
        raise SystemExit(f"CHANGELOG.md does not contain version {version}")

    readme = README_FILE.read_text(encoding="utf-8")
    if metadata["repository"] not in readme:
        raise SystemExit("README.md does not contain repository URL")


if __name__ == "__main__":
    main()
