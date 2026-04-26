from typing import Any, Dict


def build_privacy_metadata() -> Dict[str, Any]:
    """Return privacy metadata describing how the input image is handled.

    The anti-spoofing service processes the uploaded image in memory only.
    The image is not persisted by the API layer.
    """
    return {
        "privacy_first": True,
        "image_persisted": False,
        "biometric_template_stored": False,
        "raw_image_logged": False,
        "processing_scope": "in_memory_inference_only",
        "retention_policy": "no_image_retention",
    }