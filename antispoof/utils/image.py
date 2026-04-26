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
