"""Deterministically maintain the v2.3.0 release section in CHANGELOG.md."""

from __future__ import annotations

import re
from pathlib import Path

CHANGELOG_PATH = Path("CHANGELOG.md")
ANCHOR = "Global project direction is tracked in the central Age Decision repository.\n\n"
MANAGED_VERSION = "2.3.0"

CHANGELOG_SECTION_ITEMS: tuple[str, ...] = (
    "Added stable public status contract regression coverage for "
    "<code>/health</code> and <code>/model/status</code>.",
    "Standardized the public error response model to expose only "
    "<code>request_id</code>, <code>correlation_id</code>, and <code>error</code>.",
    "Normalized request validation errors to the same public ErrorResponse contract.",
    "Mapped missing multipart file validation failures to <code>missing_file</code> "
    "with HTTP 400 and <code>Invalid request.</code>.",
    "Preserved privacy-first forbidden field guarantees for anti-spoof public outputs.",
)


def build_block() -> str:
    lines = [
        f"<h2>{MANAGED_VERSION}</h2>",
        "",
        "<ul>",
    ]
    for item in CHANGELOG_SECTION_ITEMS:
        lines.append(f"  <li>{item}</li>")
    lines.extend(["</ul>", "", "<hr>", "", ""])
    return "\n".join(lines)


def main() -> None:
    heading = f"<h2>{MANAGED_VERSION}</h2>"
    new_block = build_block()
    text = CHANGELOG_PATH.read_text(encoding="utf-8")
    pattern = re.compile(
        re.escape(heading) + r"\s*\n\s*<ul>.*?</ul>\s*\n\s*<hr>\s*\n*",
        re.DOTALL,
    )
    if pattern.search(text):
        updated = pattern.sub(new_block, text, count=1)
    elif ANCHOR in text:
        updated = text.replace(ANCHOR, ANCHOR + new_block, 1)
    else:
        raise SystemExit("CHANGELOG.md missing expected anchor paragraph")

    CHANGELOG_PATH.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
