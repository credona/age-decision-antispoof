from pathlib import Path
from typing import Any

from antispoof import AntiSpoof
from antispoof.benchmark.dataset import load_benchmark_labels
from antispoof.benchmark.threshold import tune_threshold
from antispoof.domain.metrics import compute_error_rates


def run_local_benchmark(
    dataset_dir: str | Path = "benchmarks/datasets/celeba_spoof",
    threshold_step: float = 0.01,
) -> dict[str, Any]:
    """Run local benchmark evaluation and threshold tuning.

    The benchmark expects a labels.csv file and local image files.
    Dataset images are never committed to Git.
    """
    resolved_dataset_dir = Path(dataset_dir)
    labels_csv = resolved_dataset_dir / "labels.csv"

    if not labels_csv.exists():
        raise FileNotFoundError(
            f"Benchmark labels file not found: {labels_csv}. "
            "Run scripts/download_benchmark_dataset.py first."
        )

    samples = load_benchmark_labels(labels_csv)
    pipeline = AntiSpoof()

    ground_truth: list[str] = []
    predictions: list[str] = []
    real_scores: list[float] = []

    for sample in samples:
        image_path = resolved_dataset_dir / sample.image_path

        if not image_path.exists():
            raise FileNotFoundError(f"Benchmark image not found: {image_path}")

        result = pipeline.predict_from_path(image_path)

        ground_truth.append(sample.label)
        predictions.append(result.label)
        real_scores.append(result.cred_antispoof_score)

    metrics = compute_error_rates(ground_truth, predictions)
    tuning = tune_threshold(
        ground_truth_labels=ground_truth,
        real_scores=real_scores,
        step=threshold_step,
    )

    return {
        "dataset": {
            "path": str(resolved_dataset_dir),
            "labels_csv": str(labels_csv),
            "sample_count": len(samples),
        },
        "current_threshold": pipeline.threshold,
        "metrics": {
            "apcer": metrics.apcer,
            "bpcer": metrics.bpcer,
            "acer": metrics.acer,
            "attack_count": metrics.attack_count,
            "bona_fide_count": metrics.bona_fide_count,
        },
        "threshold_tuning": {
            "recommended_threshold": tuning.threshold,
            "step": threshold_step,
            "metrics": {
                "apcer": tuning.metrics.apcer,
                "bpcer": tuning.metrics.bpcer,
                "acer": tuning.metrics.acer,
                "attack_count": tuning.metrics.attack_count,
                "bona_fide_count": tuning.metrics.bona_fide_count,
            },
        },
    }
