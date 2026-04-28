import json
from pathlib import Path

PROJECT_FILE = Path("project.json")
COMPATIBILITY_FILE = Path("compatibility.json")
COMPATIBILITY_DOC_FILE = Path("docs/compatibility.md")


def main() -> None:
    project = json.loads(PROJECT_FILE.read_text(encoding="utf-8"))
    compatibility = json.loads(COMPATIBILITY_FILE.read_text(encoding="utf-8"))

    version_response = {
        "service_name": project["service_name"],
        "app_name": project["app_name"],
        "version": project["version"],
        "contract_version": project["contract_version"],
        "repository": project["repository"],
        "image": project["image"],
    }

    content = COMPATIBILITY_DOC_FILE.read_text(encoding="utf-8")
    content = replace_block(content, "VERSION_RESPONSE", version_response)
    content = replace_block(content, "COMPATIBILITY_METADATA", compatibility)

    COMPATIBILITY_DOC_FILE.write_text(content, encoding="utf-8")


def replace_block(content: str, block_name: str, payload: dict) -> str:
    start = f"<!-- BEGIN:{block_name} -->"
    end = f"<!-- END:{block_name} -->"

    if start not in content or end not in content:
        raise SystemExit(f"Missing generated block markers for {block_name}")

    before, rest = content.split(start, 1)
    _, after = rest.split(end, 1)

    generated = json.dumps(payload, indent=2, ensure_ascii=False)

    return f"{before}{start}\n```json\n{generated}\n```\n{end}{after}"


if __name__ == "__main__":
    main()
