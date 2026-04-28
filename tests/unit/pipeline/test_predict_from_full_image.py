import numpy as np
import pytest

from antispoof import AntiSpoof, FaceDetectionUnavailableError


def test_predict_from_full_image_raises_if_core_is_unavailable():
    pipeline = AntiSpoof()

    image = np.zeros((200, 200, 3), dtype=np.uint8)

    with pytest.raises(FaceDetectionUnavailableError):
        pipeline.predict_from_full_image(image)
