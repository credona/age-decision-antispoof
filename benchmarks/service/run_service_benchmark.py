from __future__ import annotations

import argparse
import time
from pathlib import Path

import requests

from antispoof.benchmark.dataset import load_benchmark_manifest
from antispoof.domain.metrics import compute_error_rates
from benchmarks.common.report import build_benchmark_report, write_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Age Decision AntiSpoof service benchmark.")
    parser.add_argument("--url", default="http://localhost:8001/check")
    parser.add_argument("--dataset-dir", default="benchmarks/datasets/celeba_spoof")
    parser.add_argument("--timeout", type=float, default=5)
    parser.add_argument("--output", default="benchmarks/reports/antispoof-service-benchmark.json")
    return parser.parse_args()


def run_service_benchmark(args: argparse.Namespace) -> dict[str, object]:
    dataset_dir = Path(args.dataset_dir)
    samples = load_benchmark_manifest(dataset_dir / "manifest.json")

    durations_ms: list[float] = []
    ground_truth: list[str] = []
    predictions: list[str] = []

    for sample in samples:
        input_path = dataset_dir / sample.image_path

        with input_path.open("rb") as file:
            start = time.perf_counter()
            response = requests.post(
                args.url,
                files={"file": (input_path.name, file, "image/jpeg")},
                timeout=args.timeout,
            )
            durations_ms.append((time.perf_counter() - start) * 1000)

        response.raise_for_status()
        payload = response.json()

        ground_truth.append(sample.label)
        predictions.append(str(payload.get("label", "spoof")))

    metrics = compute_error_rates(ground_truth, predictions)

    return build_benchmark_report(
        benchmark_target="service",
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
            "python -m benchmarks.service.run_service_benchmark "
            f"--url {args.url} --dataset-dir {args.dataset_dir} "
            f"--timeout {args.timeout} --output {args.output}"
        ),
        sample_count=len(samples),
    )


def main() -> None:
    args = parse_args()
    report = run_service_benchmark(args)
    write_report(report, args.output)
    print(f"Benchmark report written to {args.output}")


if __name__ == "__main__":
    main()
