#!/usr/bin/env bash
set -euo pipefail

./scripts/config/generate_env.sh dev

docker compose \
  --env-file .generated/compose/dev.env \
  -f docker-compose.dev.yml \
  up -d --build
