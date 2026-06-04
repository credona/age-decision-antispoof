from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

SUPPORTED_LABELS = {"real", "spoof"}


@dataclass(frozen=True)
class BenchmarkSample:
    image_path: Path
    label: str


def load_benchmark_manifest(manifest_path: str | Path) -> list[BenchmarkSample]:
    path = Path(manifest_path).resolve()

    if not path.exists():
        raise FileNotFoundError(f"Benchmark manifest file not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        raise ValueError("Benchmark manifest must be a JSON array")

    samples: list[BenchmarkSample] = []

    for index, row in enumerate(data):
        if not isinstance(row, dict):
            raise ValueError(f"Benchmark manifest row {index} must be an object")

        image_path = str(row.get("image_path", "")).strip()
        label = str(row.get("label", "")).strip()

        if not image_path:
            raise ValueError(f"Benchmark manifest row {index} is missing image_path")

        if label not in SUPPORTED_LABELS:
            raise ValueError(f"Unsupported benchmark label at row {index}: {label}")

        samples.append(BenchmarkSample(image_path=Path(image_path), label=label))

    return samples


def load_benchmark_labels(labels_path: str | Path) -> list[BenchmarkSample]:
    path = Path(labels_path)
    dataset_dir = path.parent

    if path.name == "labels.csv":
        manifest_path = dataset_dir / "manifest.json"
        if manifest_path.exists():
            return load_benchmark_manifest(manifest_path)

    resolved_csv_path = path.resolve()

    if not resolved_csv_path.exists():
        raise FileNotFoundError(f"Benchmark labels file not found: {resolved_csv_path}")

    samples: list[BenchmarkSample] = []

    with resolved_csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        required = {"image_path", "label"}

        if reader.fieldnames is None or not required.issubset(set(reader.fieldnames)):
            raise ValueError("Benchmark labels CSV is missing columns")

        for index, row in enumerate(reader, start=2):
            image_path = str(row.get("image_path", "")).strip()
            label = str(row.get("label", "")).strip()

            if not image_path:
                raise ValueError(f"Benchmark CSV line {index} is missing image_path")

            if label not in SUPPORTED_LABELS:
                raise ValueError(f"Unsupported label at CSV line {index}: {label}")

            samples.append(BenchmarkSample(image_path=Path(image_path), label=label))

    return samples
