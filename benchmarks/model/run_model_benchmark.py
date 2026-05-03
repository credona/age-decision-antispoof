from __future__ import annotations

import argparse
import time
from pathlib import Path

from antispoof import AntiSpoof
from antispoof.benchmark.dataset import load_benchmark_labels
from antispoof.domain.metrics import compute_error_rates
from benchmarks.common.report import build_benchmark_report, write_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Age Decision AntiSpoof model benchmark.")
    parser.add_argument("--dataset-dir", default="benchmarks/datasets/celeba_spoof")
    parser.add_argument("--output", default="benchmarks/reports/antispoof-model-benchmark.json")
    return parser.parse_args()


def run_model_benchmark(args: argparse.Namespace) -> dict[str, object]:
    dataset_dir = Path(args.dataset_dir)
    samples = load_benchmark_labels(dataset_dir / "labels.csv")
    pipeline = AntiSpoof()

    durations_ms: list[float] = []
    ground_truth: list[str] = []
    predictions: list[str] = []

    for sample in samples:
        input_path = dataset_dir / sample.image_path

        start = time.perf_counter()
        result = pipeline.predict_from_path(input_path)
        durations_ms.append((time.perf_counter() - start) * 1000)

        ground_truth.append(sample.label)
        predictions.append(result.label)

    metrics = compute_error_rates(ground_truth, predictions)

    return build_benchmark_report(
        benchmark_target="model",
        durations_ms=durations_ms,
        labels=predictions,
        error_rates={
            "apcer": metrics.apcer,
            "bpcer": metrics.bpcer,
            "acer": metrics.acer,
            "attack_count": metrics.attack_count,
            "bona_fide_count": metrics.bona_fide_count,
        },
        command=(
            "python -m benchmarks.model.run_model_benchmark "
            f"--dataset-dir {args.dataset_dir} --output {args.output}"
        ),
        sample_count=len(samples),
    )


def main() -> None:
    args = parse_args()
    report = run_model_benchmark(args)
    write_report(report, args.output)
    print(f"Benchmark report written to {args.output}")


if __name__ == "__main__":
    main()
