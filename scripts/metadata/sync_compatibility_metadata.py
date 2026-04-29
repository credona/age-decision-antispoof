import json
from pathlib import Path

PROJECT_FILE = Path("project.json")
COMPATIBILITY_FILE = Path("compatibility.json")


def main() -> None:
    project = json.loads(PROJECT_FILE.read_text(encoding="utf-8"))
    compatibility = json.loads(COMPATIBILITY_FILE.read_text(encoding="utf-8"))

    changed = False

    for field in ("version", "contract_version"):
        if compatibility[field] != project[field]:
            compatibility[field] = project[field]
            changed = True
            print(f"Updated compatibility.json {field} to {project[field]}")

    if changed:
        COMPATIBILITY_FILE.write_text(
            json.dumps(compatibility, indent=2) + "\n",
            encoding="utf-8",
        )
    else:
        print("compatibility.json already up-to-date")


if __name__ == "__main__":
    main()
