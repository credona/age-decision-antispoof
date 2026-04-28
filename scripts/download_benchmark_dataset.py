import argparse
import csv
import os
from collections.abc import Iterable
from pathlib import Path
from typing import Any

HF_DATASET_NAME = "nguyenkhoa/celeba-spoof-for-face-antispoofing-test"


def _write_labels_csv(
    rows: Iterable[dict[str, Any]],
    output_csv_path: Path,
) -> int:
    """Write normalized benchmark labels to CSV."""
    output_csv_path.parent.mkdir(parents=True, exist_ok=True)

    count = 0

    with output_csv_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["image_path", "label"])
        writer.writeheader()

        for row in rows:
            writer.writerow(row)
            count += 1

    return count


def _normalize_label(label_value: Any, label_names: Any | None = None) -> str:
    """Normalize dataset label into the Age Decision real/spoof contract."""
    if label_names is not None:
        normalized_names = str(label_names).lower()

        if "spoof" in normalized_names or "fake" in normalized_names:
            return "spoof"

        if "live" in normalized_names or "real" in normalized_names:
            return "real"

    if isinstance(label_value, str):
        normalized = label_value.strip().lower()

        if normalized in {"real", "live", "bona_fide", "bonafide"}:
            return "real"

        if normalized in {"spoof", "attack", "fake"}:
            return "spoof"

    if isinstance(label_value, int):
        return "real" if label_value == 0 else "spoof"

    if isinstance(label_value, list) and label_value:
        return _normalize_label(label_value[0], label_names)

    raise ValueError(f"Unsupported dataset label value: {label_value}")


def _download_celeba_spoof_from_huggingface(output_dir: Path, limit: int) -> None:
    """Download a small CelebA-Spoof-compatible subset from Hugging Face.

    This function requires the optional dependencies:
    - datasets
    - pillow

    Files are stored locally and remain outside Git.
    """
    try:
        from datasets import load_dataset
    except ImportError as exc:
        raise RuntimeError(
            "Missing optional dependency: datasets. Install it with: pip install datasets pillow"
        ) from exc

    dataset = load_dataset(
        HF_DATASET_NAME,
        split="test",
        streaming=True,
    )

    image_dir = output_dir / "images"
    image_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []

    for index, sample in enumerate(dataset):
        if index >= limit:
            break

        image = sample.get("cropped_image")
        label_value = sample.get("labels")
        label_names = sample.get("labelNames")

        if image is None:
            raise ValueError(
                f"Dataset sample does not contain a cropped_image field. "
                f"Available fields: {list(sample.keys())}"
            )

        if label_value is None and label_names is None:
            raise ValueError(
                f"Dataset sample does not contain labels or labelNames fields. "
                f"Available fields: {list(sample.keys())}"
            )

        label = _normalize_label(label_value, label_names)
        relative_path = Path("images") / f"{index:06d}_{label}.jpg"
        image_path = output_dir / relative_path

        image.convert("RGB").save(image_path)

        rows.append(
            {
                "image_path": str(relative_path),
                "label": label,
            }
        )

    count = _write_labels_csv(rows, output_dir / "labels.csv")

    print(f"Downloaded {count} benchmark samples into {output_dir}")


def main() -> None:
    """Download a benchmark dataset subset for local integration tests."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dataset",
        choices=["celeba-spoof-hf"],
        default="celeba-spoof-hf",
    )
    parser.add_argument(
        "--output-dir",
        default="benchmarks/datasets/celeba_spoof",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
    )

    args = parser.parse_args()

    output_dir = Path(args.output_dir)

    if args.limit <= 0:
        raise ValueError("Limit must be greater than zero.")

    if args.dataset == "celeba-spoof-hf":
        _download_celeba_spoof_from_huggingface(output_dir, args.limit)


if __name__ == "__main__":
    main()
    os._exit(0)
