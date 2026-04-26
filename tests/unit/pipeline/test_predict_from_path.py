import cv2
import numpy as np

from antispoof import AntiSpoof, AntiSpoofResult


def test_predict_from_path_returns_expected_structure(tmp_path):
    image_path = tmp_path / "face_crop.jpg"
    fake_face_crop = np.zeros((80, 80, 3), dtype=np.uint8)

    cv2.imwrite(str(image_path), fake_face_crop)

    pipeline = AntiSpoof()
    result = pipeline.predict_from_path(image_path)

    assert isinstance(result, AntiSpoofResult)

    assert isinstance(result.is_real, bool)
    assert isinstance(result.confidence, float)
    assert isinstance(result.scores, list)
    assert result.label in ["real", "spoof"]