from pathlib import Path

import cv2
import numpy as np


def read_image(path: str | Path) -> np.ndarray:
    """Read an image from disk as a BGR OpenCV array."""
    image_path = Path(path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError(f"Unable to read image: {image_path}")

    return image


def read_image_from_bytes(image_bytes: bytes):
    """Read an OpenCV image from encoded image bytes."""
    import cv2
    import numpy as np

    if not image_bytes:
        raise ValueError("Empty image bytes.")

    image_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Invalid image bytes.")

    return image
