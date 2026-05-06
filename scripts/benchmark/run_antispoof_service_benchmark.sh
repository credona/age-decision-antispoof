#!/usr/bin/env sh
set -eu

URL="${BENCHMARK_ANTISPOOF_URL:-http://localhost:8001/check}"
DATASET_DIR="${BENCHMARK_DATASET_DIR:-benchmarks/datasets/celeba_spoof}"
TIMEOUT="${BENCHMARK_TIMEOUT:-5}"
OUTPUT_PATH="${BENCHMARK_OUTPUT_PATH:-benchmarks/reports/antispoof-service-benchmark.json}"

python -m benchmarks.service.run_service_benchmark   --url "$URL"   --dataset-dir "$DATASET_DIR"   --timeout "$TIMEOUT"   --output "$OUTPUT_PATH"
