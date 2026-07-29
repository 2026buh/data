import cv2 


def apply_jpeg_compression(img, rng, cfg):
    quality = int(
        rng.integers(
            cfg["quality_range"][0],
            cfg["quality_range"][1] + 1
        )
    )

img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

success, encoded = cv2.imencode(
    ".jpg",
    img_bgr,
    [int(cv2.IMWRITE_JPEG_QUALITY), quality]
)

if not success:
    raise RuntimeError("JPEG encoding failed.")

decoded_bgr = cv2.imdecode(encoded, cv2.IMREAD_COLOR)

if decoded_bgr is None:
    raise RuntimeError("JPEG decoding failed.")

out = cv2.cvtColor(decoded_bgr, cv2.Color_BGR2RGB)

return out, { 
    "jpeg_quality": quality
}