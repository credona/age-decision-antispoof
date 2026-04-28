import json
import os
from pathlib import Path

PROJECT_FILE = Path("project.json")


def main() -> None:
    metadata = json.loads(PROJECT_FILE.read_text(encoding="utf-8"))

    expected_tag = f"v{metadata['version']}"
    github_ref_type = os.getenv("GITHUB_REF_TYPE")
    github_ref_name = os.getenv("GITHUB_REF_NAME")

    if github_ref_type != "tag":
        print("Release metadata check skipped because this is not a tag build.")
        return

    if github_ref_name != expected_tag:
        raise SystemExit(f"Release tag mismatch: expected {expected_tag}, got {github_ref_name}")

    print(f"Release metadata check passed for {expected_tag}.")


if __name__ == "__main__":
    main()
