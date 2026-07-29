import numpy as np

def clip_uint8(x):
    return np.clip(x, 0, 255).astype(np.uint8)

def random_signed_factor(rng, delta_range):
    delta = float(rng.uniform(*delta_range))
    sign = float(rng.choice([-1, 1]))
    return 1.0 + sign * delta

def apply_brightness_contrast(img, rng, cfg):
    brightness = random_signed_factor(rng, cfg["brightness_delta_range"])
    contrast = random_signed_factor(rng, cfg["contrast_delta_range"])

    out = img.astype(np.float32)
    out *= rightness

    mean = np.mean(out, axis=(0,1), keepdims=True)
    out =  (out - mean) * contrast + mean
    
    return clip_uint8(out), {
        "brightness": brightness,
        "contrast": contrast
    }