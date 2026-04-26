import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List


SUPPORTED_LABELS = {"real", "spoof"}


@dataclass(frozen=True)
class BenchmarkSample:
    """Represents one benchmark image and its ground truth label."""

    image_path: Path
    label: str


def load_benchmark_labels(csv_path: str | Path) -> List[BenchmarkSample]:
    """Load benchmark samples from a CSV file.

    Expected CSV columns:
    - image_path
    - label

    Supported labels:
    - real
    - spoof
    """
    resolved_csv_path = Path(csv_path)

    if not resolved_csv_path.exists():
        raise FileNotFoundError(f"Benchmark labels file not found: {resolved_csv_path}")

    samples: List[BenchmarkSample] = []

    with resolved_csv_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames is None:
            raise ValueError("Benchmark labels CSV must contain a header.")

        required_columns = {"image_path", "label"}
        missing_columns = required_columns - set(reader.fieldnames)

        if missing_columns:
            raise ValueError(
                f"Benchmark labels CSV is missing columns: {sorted(missing_columns)}"
            )

        for row_index, row in enumerate(reader, start=2):
            image_path = row["image_path"].strip()
            label = row["label"].strip().lower()

            if not image_path:
                raise ValueError(f"Missing image_path at CSV line {row_index}")

            if label not in SUPPORTED_LABELS:
                raise ValueError(
                    f"Unsupported label at CSV line {row_index}: {label}"
                )

            samples.append(
                BenchmarkSample(
                    image_path=Path(image_path),
                    label=label,
                )
            )

    return samples