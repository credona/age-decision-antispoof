from __future__ import annotations

import os
import platform
import shutil
import subprocess


def collect_machine_metadata() -> dict[str, object]:
    return {
        "cpu": _cpu_name(),
        "ram_gb": _ram_gb(),
        "gpu": os.getenv("BENCHMARK_GPU", ""),
        "hosting_provider": os.getenv("BENCHMARK_HOSTING_PROVIDER", "local"),
        "os": platform.platform(),
        "docker_version": _docker_version(),
    }


def _cpu_name() -> str:
    if platform.system().lower() == "linux":
        try:
            with open("/proc/cpuinfo", encoding="utf-8") as file:
                for line in file:
                    if line.startswith("model name"):
                        return line.split(":", 1)[1].strip()
        except OSError:
            pass

    return platform.processor() or platform.machine() or "unknown"


def _ram_gb() -> float:
    if platform.system().lower() == "linux":
        try:
            with open("/proc/meminfo", encoding="utf-8") as file:
                for line in file:
                    if line.startswith("MemTotal:"):
                        return round(int(line.split()[1]) / 1024 / 1024, 2)
        except OSError:
            pass

    return 0.0


def _docker_version() -> str:
    if shutil.which("docker") is None:
        return "unavailable"

    try:
        result = subprocess.run(
            ["docker", "--version"],
            check=False,
            capture_output=True,
            text=True,
            timeout=3,
        )
    except (OSError, subprocess.TimeoutExpired):
        return "unavailable"

    return result.stdout.strip() or "unavailable"
