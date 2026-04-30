import json
from pathlib import Path

PROJECT_FILE = Path("project.json")
COMPATIBILITY_FILE = Path("compatibility.json")
README_FILE = Path("README.md")


def main() -> None:
    metadata = json.loads(PROJECT_FILE.read_text(encoding="utf-8"))
    compatibility = json.loads(COMPATIBILITY_FILE.read_text(encoding="utf-8"))

    health_response = {
        "status": "ok",
        "service": metadata["service_name"],
        "version": metadata["version"],
        "contract_version": metadata["contract_version"],
    }

    version_response = {
        "service_name": metadata["service_name"],
        "app_name": metadata["app_name"],
        "version": metadata["version"],
        "contract_version": metadata["contract_version"],
        "repository": metadata["repository"],
        "image": metadata["image"],
    }

    readme = README_FILE.read_text(encoding="utf-8")
    readme = replace_block(readme, "HEALTH_RESPONSE", health_response)
    readme = replace_block(readme, "VERSION_RESPONSE", version_response)
    readme = replace_block(readme, "COMPATIBILITY_METADATA", compatibility)

    README_FILE.write_text(readme, encoding="utf-8")


def replace_block(content: str, block_name: str, payload: dict) -> str:
    start = f"<!-- BEGIN:{block_name} -->"
    end = f"<!-- END:{block_name} -->"

    if start not in content or end not in content:
        return content

    before, rest = content.split(start, 1)
    _, after = rest.split(end, 1)

    generated = json.dumps(payload, indent=2, ensure_ascii=False)

    return f"{before}{start}\n```json\n{generated}\n```\n{end}{after}"


if __name__ == "__main__":
    main()
