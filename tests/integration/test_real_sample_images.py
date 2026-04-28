from pathlib import Path

import pytest

from antispoof import AntiSpoof
from antispoof.benchmark import load_benchmark_labels
from antispoof.metrics import compute_error_rates

DATASET_DIR = Path("benchmarks/datasets/celeba_spoof")
LABELS_CSV = DATASET_DIR / "labels.csv"


@pytest.mark.integration
def test_real_benchmark_sample_images():
    """Run anti-spoofing inference on real local benchmark images.

    The test is skipped when the benchmark dataset is not available locally.
    """
    if not LABELS_CSV.exists():
        pytest.skip(
            "Real benchmark dataset not found. Run scripts/download_benchmark_dataset.py first."
        )

    samples = load_benchmark_labels(LABELS_CSV)
    pipeline = AntiSpoof()

    ground_truth: list[str] = []
    predictions: list[str] = []

    for sample in samples:
        image_path = DATASET_DIR / sample.image_path

        if not image_path.exists():
            pytest.skip(f"Benchmark image not found: {image_path}")

        result = pipeline.predict_from_path(image_path)

        ground_truth.append(sample.label)
        predictions.append(result.label)

    metrics = compute_error_rates(ground_truth, predictions)

    assert 0.0 <= metrics.apcer <= 1.0
    assert 0.0 <= metrics.bpcer <= 1.0
    assert 0.0 <= metrics.acer <= 1.0
