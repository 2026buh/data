import numpy as np
from PIL import Image

def read_image_rgb(path, resize_to=None):
    img = Image.open(path).convert("RGB")

    if resize_to is not None:
        img = img.resize(
            resize_to,
            Image.Resampling.BILINEAR
        )

    return np.array(img, dtype=np.uint8)