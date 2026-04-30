from __future__ import annotations

import argparse
import re
from pathlib import Path

CHANGELOG_PATH = Path("CHANGELOG.md")


def extract_release_body(changelog: str, version: str) -> str:
    heading = f"<h2>{version}</h2>"
    pattern = re.compile(
        re.escape(heading) + r"\s*\n(?P<body>.*?)(?:\n\s*<h2>|$)",
        re.DOTALL,
    )
    match = pattern.search(changelog)
    if not match:
        raise SystemExit(f"Version section not found in CHANGELOG.md: {version}")
    body = match.group("body").strip()
    if body.endswith("<hr>"):
        body = body[: -len("<hr>")].rstrip()
    return body


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    args = parser.parse_args()

    changelog = CHANGELOG_PATH.read_text(encoding="utf-8")
    print(extract_release_body(changelog, args.version))


if __name__ == "__main__":
    main()
