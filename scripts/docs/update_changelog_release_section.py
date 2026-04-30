"""Deterministically maintain the v2.2.3 release section in CHANGELOG.md."""

from __future__ import annotations

import re
from pathlib import Path

CHANGELOG_PATH = Path("CHANGELOG.md")
ANCHOR = "Global project direction is tracked in the central Age Decision repository.\n\n"
MANAGED_VERSION = "2.2.3"

CHANGELOG_SECTION_ITEMS: tuple[str, ...] = (
    "Enforced documentation boundaries between global and repository-specific docs.",
    "Removed cross-repository documentation duplication.",
    "Normalized repository <code>README.md</code> scope.",
    "Normalized <code>CONTRIBUTING.md</code> to local workflows.",
    "Normalized <code>SECURITY.md</code> and <code>COMPATIBILITY.md</code> scope.",
    "Enforced absolute GitHub links only for cross-repository documentation references.",
    "Centralized global documentation in <code>age-decision</code>.",
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
