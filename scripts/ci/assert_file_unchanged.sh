#!/usr/bin/env bash
set -euo pipefail

FILE="$1"
shift

TMP_FILE="$(mktemp)"
cp "$FILE" "$TMP_FILE"

"$@"

if ! cmp -s "$FILE" "$TMP_FILE"; then
  echo "Generated file is outdated: $FILE"
  echo "Run the related update script and commit the result."
  exit 1
fi

rm -f "$TMP_FILE"
