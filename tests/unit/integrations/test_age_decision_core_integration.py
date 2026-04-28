import sys
import types

import numpy as np

from antispoof import AntiSpoof


class FakeFaceDetector:
    """Mocked FaceDetector to simulate age-decision-core behavior."""

    def detect(self, image):
        """Return a single fake face bounding box."""
        h, w, _ = image.shape
        return [(0, 0, w // 2, h // 2)]


def test_predict_from_full_image_with_mocked_core():
    fake_module = types.ModuleType("age_decision_core")
    fake_module.FaceDetector = FakeFaceDetector

    previous_module = sys.modules.get("age_decision_core")
    sys.modules["age_decision_core"] = fake_module

    try:
        pipeline = AntiSpoof()

        image = np.zeros((200, 200, 3), dtype=np.uint8)
        result = pipeline.predict_from_full_image(image)

        assert result is not None
        assert hasattr(result, "is_real")
        assert hasattr(result, "confidence")
    finally:
        if previous_module is not None:
            sys.modules["age_decision_core"] = previous_module
        else:
            sys.modules.pop("age_decision_core", None)
