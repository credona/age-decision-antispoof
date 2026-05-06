import json
from pathlib import Path

import pytest

from antispoof.benchmark.dataset import load_benchmark_labels, load_benchmark_manifest


def test_load_benchmark_manifest(tmp_path: Path):
    dataset = tmp_path / "dataset"
    dataset.mkdir()

    (dataset / "manifest.json").write_text(
        json.dumps(
            [
                {"image_path": "images/real.jpg", "label": "real"},
                {"image_path": "images/spoof.jpg", "label": "spoof"},
            ]
        ),
        encoding="utf-8",
    )

    samples = load_benchmark_manifest(dataset / "manifest.json")

    assert len(samples) == 2
    assert samples[0].image_path == Path("images/real.jpg")
    assert samples[0].label == "real"


def test_load_benchmark_labels_prefers_manifest_over_csv(tmp_path: Path):
    dataset = tmp_path / "dataset"
    dataset.mkdir()

    (dataset / "labels.csv").write_text(
        "image_path,label\nlegacy.jpg,real\n",
        encoding="utf-8",
    )

    (dataset / "manifest.json").write_text(
        json.dumps([{"image_path": "images/current.jpg", "label": "spoof"}]),
        encoding="utf-8",
    )

    samples = load_benchmark_labels(dataset / "labels.csv")

    assert len(samples) == 1
    assert samples[0].image_path == Path("images/current.jpg")
    assert samples[0].label == "spoof"


def test_load_benchmark_manifest_rejects_invalid_label(tmp_path: Path):
    dataset = tmp_path / "dataset"
    dataset.mkdir()

    (dataset / "manifest.json").write_text(
        json.dumps([{"image_path": "images/file.jpg", "label": "unknown"}]),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unsupported benchmark label"):
        load_benchmark_manifest(dataset / "manifest.json")
