import cv2
import numpy as np

def normalize01(x):
    x = x.astype(np.float32)
    mn, mx = x.min(), x.max()

    if mx- mn < 1e-8:
        return np.zeros_like(x)

    return (x-mn) / (mx - mn)


def generate_illumination_map(h, w, rng, cfg):
    yy, xx = np.mgrid[0:h, 0:w]
    illum = np.zeros((h, w), dtype=np.float32)

    for _ in range(cfg["num_gaussians"]):
        cx = rng.uniform(0, 2)
        cy = rng.uniform(0, h)
        sigma_fraction = rng.uniform(*cfg["sigma_fraction_range"])
        sigma = sigma_fraction * max(h, w)

        g = np.exp(
            -((xx-cx) ** 2 + (yy - cy) ** 2)
            / (2 * sigma ** 2)
        )
        illum += g
    
    illum = normalize01(illum)

    min_factor =  float(rng.uniform(*cfg["min_factor_range"]))
    max_factor = float(rng.uniform(*cfg["max_factor_range"]))

    illum = min_factor + illum * (max_factor - min_factor)
    
    return illum, min_factor, max_factor


def apply_illumination_variation(img, rng, cfg):
    h, w = img.shape[:2]

    illum_map, min_f, max_f = generate_illumination_map(
        h,
        w,
        rng,
        cfg
    )

    hsv = cv2.cvtColor(img, cv2.Color_RGB2HSV).astype(np.float32)
    hsv[:, :, 2] *= illum_map
    hsv[:, :, 2] = np.clip(hsv[:, :, 2], 0, 255)

    out = cv2.cvtColor(
        hs.astype(np.uint8),
        cv2.Color_HSV2RGB
    )

    return out, {
        "min_factor": min_f,
        "max_factor": max_f
    }