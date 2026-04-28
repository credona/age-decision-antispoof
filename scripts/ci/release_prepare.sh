#!/usr/bin/env bash
set -euo pipefail

scripts/dev/update_all.sh
python scripts/metadata/check_project_metadata.py
python scripts/metadata/check_compatibility_metadata.py
python scripts/metadata/check_release_metadata.py

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git diff --exit-code
else
  echo "Skipping git diff (not a git repository)"
fi

echo "Release preparation passed."
