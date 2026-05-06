# AntiSpoof Benchmarks

This directory contains Age Decision AntiSpoof benchmark tooling for v2.6.0.

## Scope

AntiSpoof benchmarks cover:

- local model execution
- HTTP service execution
- aggregate anti-spoof error rates
- privacy-safe report generation
- deterministic benchmark metadata

## Reports

Reports are written as JSON and must follow:

benchmarks/schemas/benchmark-report.schema.json

## Privacy

Benchmark reports must never expose:

- raw scores
- internal thresholds
- score components
- local image paths
- manifest raw content
- base64 payloads
- raw payloads
- downstream raw responses
- model paths

Only aggregate metrics are allowed.

## Datasets

Benchmark datasets are not bundled by default.

Generic dataset format documentation is available in:

benchmarks/datasets/README.md

Dataset-specific instructions are available inside each dataset directory.

Example:

benchmarks/datasets/celeba_spoof/README.md

## Model benchmark

Run:

scripts/benchmark/run_antispoof_model_benchmark.sh

## Service benchmark

Start the service first, then run:

scripts/benchmark/run_antispoof_service_benchmark.sh

## All benchmarks

Run model benchmark only:

scripts/benchmark/run_all.sh

Run model and service benchmarks:

BENCHMARK_RUN_SERVICE=true scripts/benchmark/run_all.sh
