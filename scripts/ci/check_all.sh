#!/usr/bin/env bash
set -euo pipefail

ruff check .
ruff format --check .

if grep -rIn "[[:blank:]]$" antispoof tests scripts docs README.md CHANGELOG.md CONTRIBUTING.md; then
  echo "Trailing whitespace found"
  exit 1
fi

FAILED=0

for file in $(find antispoof tests scripts docs -type f \( -name "*.py" -o -name "*.md" -o -name "*.sh" \)); do
  if [ -s "$file" ] && [ "$(tail -c1 "$file")" != "" ]; then
    echo "Missing final newline: $file"
    FAILED=1
  fi
done

for file in README.md CHANGELOG.md CONTRIBUTING.md pyproject.toml project.json compatibility.json; do
  if [ -f "$file" ] && [ -s "$file" ] && [ "$(tail -c1 "$file")" != "" ]; then
    echo "Missing final newline: $file"
    FAILED=1
  fi
done

if [ "$FAILED" -ne 0 ]; then
  exit "$FAILED"
fi

python -m compileall antispoof tests scripts
python scripts/metadata/check_project_metadata.py
python scripts/metadata/check_compatibility_metadata.py
python scripts/docs/update_readme_examples.py
git diff --exit-code README.md
python scripts/docs/update_docs_usage.py
git diff --exit-code docs/usage.md
python scripts/docs/update_docs_compatibility.py
git diff --exit-code docs/compatibility.md
pytest
pytest tests/unit/contract
pytest tests/unit/privacy
pytest tests/unit/api/test_public_api.py

echo "CI-equivalent check passed."
