import json
import re
from pathlib import Path

PROJECT_FILE = Path("project.json")
DOCKERFILE = Path("Dockerfile")

REQUIRED_LABELS = {
    "org.opencontainers.image.title",
    "org.opencontainers.image.description",
    "org.opencontainers.image.version",
    "org.opencontainers.image.licenses",
    "org.opencontainers.image.source",
}


def main() -> None:
    project = json.loads(PROJECT_FILE.read_text(encoding="utf-8"))
    dockerfile = DOCKERFILE.read_text(encoding="utf-8")

    labels = extract_labels(dockerfile)

    missing = sorted(REQUIRED_LABELS - labels.keys())
    if missing:
        raise SystemExit(f"Missing Docker OCI labels: {', '.join(missing)}")

    assert_dynamic_or_equal(
        "Docker image version",
        labels["org.opencontainers.image.version"],
        project["version"],
        "${VERSION}",
    )

    assert_dynamic_or_equal(
        "Docker image source",
        labels["org.opencontainers.image.source"],
        project["repository"],
        "${REPOSITORY}",
    )

    assert_dynamic_or_equal(
        "Docker image license",
        labels["org.opencontainers.image.licenses"],
        project["license"],
        "${LICENSE}",
    )

    if not labels["org.opencontainers.image.title"]:
        raise SystemExit("Docker image title must not be empty")

    if not labels["org.opencontainers.image.description"]:
        raise SystemExit("Docker image description must not be empty")

    print("Docker metadata check passed.")


def extract_labels(dockerfile: str) -> dict[str, str]:
    labels: dict[str, str] = {}

    for match in re.finditer(
        r'([\w.-]+)="([^"]*)"',
        dockerfile,
    ):
        key, value = match.groups()
        if key.startswith("org.opencontainers.image."):
            labels[key] = value

    return labels


def assert_dynamic_or_equal(name: str, actual: str, expected: str, variable: str) -> None:
    if actual not in {expected, variable}:
        raise SystemExit(f"{name} mismatch: expected {expected} or {variable}, got {actual}")


if __name__ == "__main__":
    main()
