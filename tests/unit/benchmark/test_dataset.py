from pathlib import Path

import pytest

from antispoof.benchmark import load_benchmark_labels


def test_load_benchmark_labels(tmp_path):
    """Test benchmark CSV loading."""
    csv_path = tmp_path / "labels.csv"
    csv_path.write_text(
        "image_path,label\n"
        "real/001.jpg,real\n"
        "spoof/001.jpg,spoof\n",
        encoding="utf-8",
    )

    samples = load_benchmark_labels(csv_path)

    assert len(samples) == 2
    assert samples[0].image_path == Path("real/001.jpg")
    assert samples[0].label == "real"
    assert samples[1].image_path == Path("spoof/001.jpg")
    assert samples[1].label == "spoof"


def test_load_benchmark_labels_rejects_missing_file():
    """Test benchmark CSV missing file handling."""
    with pytest.raises(FileNotFoundError):
        load_benchmark_labels("missing.csv")


def test_load_benchmark_labels_rejects_missing_columns(tmp_path):
    """Test benchmark CSV required columns validation."""
    csv_path = tmp_path / "labels.csv"
    csv_path.write_text(
        "path,target\n"
        "real/001.jpg,real\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError) as exc:
        load_benchmark_labels(csv_path)

    assert "Benchmark labels CSV is missing columns" in str(exc.value)


def test_load_benchmark_labels_rejects_invalid_label(tmp_path):
    """Test benchmark CSV label validation."""
    csv_path = tmp_path / "labels.csv"
    csv_path.write_text(
        "image_path,label\n"
        "unknown/001.jpg,unknown\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError) as exc:
        load_benchmark_labels(csv_path)

    assert str(exc.value) == "Unsupported label at CSV line 2: unknown"