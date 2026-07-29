import cv2
import numpy as np

def clip_uint8(x):
    return np.clip(x, 0, 255).astype(np.uint8)


def normalize(x):
    x = x.astype(np.float32)
    mn, mx = x.min(), x.max()

    if mx - mn < 1e-8:
        return np.zeros_like(x)


    return (x - mn)/ (mx - mn)

def apply_dark_spots(img, rng, cfg):
    h, w = img.shape[:2]
    out = img.astype(np.float32).copy()
    yy, xx = np.mgrid[0:h, 0:w]

    n_spots = int(
        rng.integers(
            cfg["num_spots_range"][0],
            cfg["num_spots_range"][1] + 1
        
        )
    )

for _ in range(n_spots):
    radius = float(rng.uniform(*cfg["radius_range"]))
    opacity = float(rng.uniform(*cfg["opacity_range"]))
    softness = float(rng.uniform(*cfg["edge_softness_range"]))

    cx = float(rng.uniform(-radius, w + radius))
    cy = float(rng.uniform(-radius, h + radius))

    dist = np.sqrt((xx-cx) **2 + (yy-cy) ** 2)

    sigma = radius * softness
    mask = np.exp(-(dist **2) / 2 * sigma ** 2)
    mask = mask ** rng.uniform(0.8, 1.4)
    mask = np.clip(mask, 0, 1)

    noise = rng.normal(0, 1, size=(h, w)).astype(np.float32)
    noise = normalize01(noise)
    noise = cv2.GaussianBlur(
        noise, 
        ksize=(0,0)
        sigmaX=max(radius * 0.45, 2),
        sigmaY=max(radius * 0.45, 2)
    )
    irregularity_strength = rng.uniform(0.05, 0.20)
    mask = mask * (
        1.0
        - irregularity_strength
        +irregularity_strength * noise
    )
    mask = np.clip(mask, 0, 1)

    spot_value = rng.uniform(0, 18)
    spot_color = np.array(
        [spot_value, spot_value, spot_value],
        dtype=np.float32
    )

    alpha = opacity * mask[:, :, None]
    out = out * (1 - alpha) + spot_color * alpha

return clip_uint8(out), {"num_spots": n_spots}