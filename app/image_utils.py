from PIL import Image
import numpy as np


def resize_max(img: Image.Image, max_size: int = 150) -> Image.Image:
    """Resize image so its largest dimension is max_size, preserving aspect ratio."""
    w, h = img.size
    scale = min(max_size / w, max_size / h)
    new_w, new_h = int(w * scale), int(h * scale)
    return img.resize((new_w, new_h), Image.BILINEAR)


def image_to_array(img: Image.Image) -> np.ndarray:
    """Convert PIL image to numpy array."""
    return np.array(img, dtype=np.uint8)
