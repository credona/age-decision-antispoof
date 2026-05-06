from __future__ import annotations

import hashlib
import json
import os
import statistics
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from antispoof.project import project_metadata
from benchmarks.common.machine import collect_machine_metadata

BENCHMARK_VERSION = "2.6.0"

FORBIDDEN_KEYS = {
    "estimated_age",
    "confidence",
    "raw_score",
    "raw_scores",
    "threshold",
    "thresholds",
    "internal_thresholds",
    "score_components",
    "model_path",
    "image",
    "base64",
    "payload",
    "downstream_response",
    "downstream_raw_response",
    "raw_response",
    "labels_csv",
    "path",
}


def build_benchmark_report(
    *,
    benchmark_target: str,
    durations_ms: list[float],
    labels: Iterable[str],
    error_rates: dict[str, float | int],
    command: str,
    sample_count: int,
) -> dict[str, Any]:
    timestamp = _generated_at()
    seed = int(os.getenv("BENCHMARK_SEED", "2600"))

    dataset_id = os.getenv("BENCHMARK_DATASET_ID", "local_antispoof_smoke")
    benchmark_id = os.getenv(
        "BENCHMARK_ID",
        f"age-decision-antispoof-{benchmark_target}-{dataset_id}",
    )

    label_distribution = {"real": 0, "spoof": 0}

    for label in labels:
        if label in label_distribution:
            label_distribution[label] += 1

    report: dict[str, Any] = {
        "benchmark_id": benchmark_id,
        "benchmark_version": BENCHMARK_VERSION,
        "benchmark_target": benchmark_target,
        "dataset_id": dataset_id,
        "generated_at": timestamp,
        "model": os.getenv("BENCHMARK_MODEL", "age-decision-antispoof"),
        "service": "antispoof",
        "dataset": {
            "name": os.getenv("BENCHMARK_DATASET_NAME", "local-antispoof-smoke"),
            "version": os.getenv("BENCHMARK_DATASET_VERSION", "0.0.0"),
            "split": os.getenv("BENCHMARK_DATASET_SPLIT", "validation"),
            "sample_count": sample_count,
            "license": os.getenv("BENCHMARK_DATASET_LICENSE", "not-distributed"),
            "source_reference": os.getenv(
                "BENCHMARK_DATASET_SOURCE",
                "local benchmark asset",
            ),
            "manifest_hash_sha256": os.getenv(
                "BENCHMARK_MANIFEST_HASH_SHA256",
                "0" * 64,
            ),
        },
        "machine": _machine_metadata(),
        "metrics": {
            "latency_ms_avg": _mean(durations_ms),
            "latency_ms_p95": _p95(durations_ms),
            "throughput_rps": _throughput(durations_ms),
            "sample_count": sample_count,
            "label_distribution": label_distribution,
            "error_rates": {
                "apcer": float(error_rates.get("apcer", 0.0)),
                "bpcer": float(error_rates.get("bpcer", 0.0)),
                "acer": float(error_rates.get("acer", 0.0)),
                "attack_count": int(error_rates.get("attack_count", 0)),
                "bona_fide_count": int(error_rates.get("bona_fide_count", 0)),
            },
            "service_version": project_metadata.version,
            "contract_version": project_metadata.contract_version,
            "command_hash_sha256": _stable_command_hash(command),
        },
        "privacy": {
            "contains_raw_image": False,
            "contains_base64": False,
            "contains_downstream_raw_response": False,
            "contains_internal_thresholds": False,
            "contains_estimated_age": False,
            "contains_raw_scores": False,
        },
        "run": {
            "timestamp": timestamp,
            "seed": seed,
        },
    }

    assert_report_is_privacy_safe(report)
    return report


def write_report(report: dict[str, Any], output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def assert_report_is_privacy_safe(report: dict[str, Any]) -> None:
    _assert_no_forbidden_keys(report)

    privacy = report.get("privacy")
    if not isinstance(privacy, dict):
        raise ValueError("Missing benchmark privacy metadata")

    for key, value in privacy.items():
        if key.startswith("contains_") and value is not False:
            raise ValueError(f"Invalid benchmark privacy flag: {key}")


def _assert_no_forbidden_keys(value: Any) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key.lower() in FORBIDDEN_KEYS:
                raise ValueError(f"Forbidden benchmark report field detected: {key}")
            _assert_no_forbidden_keys(item)
    elif isinstance(value, list):
        for item in value:
            _assert_no_forbidden_keys(item)


def _generated_at() -> str:
    return (
        os.getenv("BENCHMARK_GENERATED_AT") or datetime.now(UTC).replace(microsecond=0).isoformat()
    )


def _machine_metadata() -> dict[str, Any]:
    machine = collect_machine_metadata()

    return {
        "cpu": str(machine.get("cpu", "unknown")),
        "ram_gb": float(machine.get("ram_gb", 0.0)),
        "gpu": str(machine.get("gpu", os.getenv("BENCHMARK_GPU", "none"))),
        "hosting_provider": str(
            machine.get(
                "hosting_provider",
                os.getenv("BENCHMARK_HOSTING_PROVIDER", "unknown"),
            )
        ),
        "os": str(machine.get("os", "unknown")),
        "docker_version": str(machine.get("docker_version", "unavailable")),
    }


def _stable_command_hash(command: str) -> str:
    return hashlib.sha256(command.encode("utf-8")).hexdigest()


def _mean(values: list[float]) -> float:
    return round(statistics.mean(values), 4) if values else 0.0


def _p95(values: list[float]) -> float:
    if not values:
        return 0.0

    ordered = sorted(values)
    index = max(0, min(len(ordered) - 1, int(len(ordered) * 0.95) - 1))
    return round(ordered[index], 4)


def _throughput(durations_ms: list[float]) -> float:
    total_seconds = sum(durations_ms) / 1000

    if total_seconds <= 0:
        return 0.0

    return round(len(durations_ms) / total_seconds, 4)
