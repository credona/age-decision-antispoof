"""Anti-spoofing benchmark metrics."""

from antispoof.metrics.error_rates import (
    AntiSpoofMetrics,
    compute_error_rates,
)

__all__ = [
    "AntiSpoofMetrics",
    "compute_error_rates",
]