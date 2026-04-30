"""Deterministically maintain the v2.2.2 release section in CHANGELOG.md."""

from __future__ import annotations

import re
from pathlib import Path

CHANGELOG_PATH = Path("CHANGELOG.md")
ANCHOR = "Global project direction is tracked in the central Age Decision repository.\n\n"
MANAGED_VERSION = "2.2.2"

CHANGELOG_SECTION_ITEMS: tuple[str, ...] = (
    (
        "Published Docker images from version tags only; pull request workflows no "
        "longer publish Docker images."
    ),
    (
        "Release workflow builds GitHub release description from the matching "
        "<code>CHANGELOG.md</code> section."
    ),
    (
        "Release workflow validates the Git tag matches <code>project.json</code> "
        "and that exactly one GHCR package version carries that tag."
    ),
    "Added manual and scheduled workflow to delete untagged GHCR Docker package versions.",
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
