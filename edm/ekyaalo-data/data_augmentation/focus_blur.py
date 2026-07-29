import cv2

def apply_focus_blur(img, rng, cfg, global_cfg):
    sigma = float(rng.uniform(*cfg["sigma_range"]))
    sigma *= float(global_cfg.get("blur_scale", 1.0))

    out = cv2.GaussianBlur(
        img,
        ksize=(0, 0),
        sigmaX=sigma,
        sigmaY=sigma
    )

    return out, {"sigma": sigma}