import cv2
import numpy as np


def resize_face_crop(face_image: np.ndarray, size: tuple[int, int] = (80, 80)) -> np.ndarray:
    """Resize a face crop to the model input size."""
    if face_image is None or face_image.size == 0:
        raise ValueError("Face image is empty.")

    return cv2.resize(face_image, size)
