#!/usr/bin/env bash
set -euo pipefail

PROFILE="${1:-prod}"

./scripts/config/generate_env.sh "$PROFILE"

docker compose \
  --env-file ".generated/compose/$PROFILE.env" \
  -f docker-compose.dev.yml \
  build
