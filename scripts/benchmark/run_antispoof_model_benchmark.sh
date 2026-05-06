#!/usr/bin/env sh
set -eu

DATASET_DIR="${BENCHMARK_DATASET_DIR:-benchmarks/datasets/celeba_spoof}"
OUTPUT_PATH="${BENCHMARK_OUTPUT_PATH:-benchmarks/reports/antispoof-model-benchmark.json}"

python -m benchmarks.model.run_model_benchmark   --dataset-dir "$DATASET_DIR"   --output "$OUTPUT_PATH"
