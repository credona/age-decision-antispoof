#!/usr/bin/env sh
set -eu

scripts/benchmark/run_antispoof_model_benchmark.sh

if [ "${BENCHMARK_RUN_SERVICE:-false}" = "true" ]; then
  scripts/benchmark/run_antispoof_service_benchmark.sh
fi
