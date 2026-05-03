from typing import Any

from antispoof.domain.constants import (
    PROCESSING_SCOPE_IN_MEMORY,
    RETENTION_POLICY_NO_IMAGE,
)


def build_privacy_metadata() -> dict[str, Any]:
    """Return privacy metadata describing how the input image is handled.

    The anti-spoofing service processes the uploaded image in memory only.
    The image is not persisted by the API layer.
    """
    return {
        "privacy_first": True,
        "image_persisted": False,
        "biometric_template_stored": False,
        "raw_image_logged": False,
        "processing_scope": PROCESSING_SCOPE_IN_MEMORY,
        "retention_policy": RETENTION_POLICY_NO_IMAGE,
    }
