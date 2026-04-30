#!/usr/bin/env bash
set -euo pipefail

ruff check .
ruff format --check .

python -m compileall antispoof tests scripts

scripts/dev/update_all.sh

python scripts/metadata/check_project_metadata.py
python scripts/metadata/check_compatibility_metadata.py

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git diff --exit-code README.md docs/usage.md docs/compatibility.md compatibility.json CHANGELOG.md
else
  echo "Skipping git diff (not a git repository)"
fi

pytest

echo "Local check passed."
