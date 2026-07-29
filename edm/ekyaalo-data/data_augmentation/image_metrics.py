import cv2
import numpy as np
from skimmage.metrics import structural_similarity as compare_ssim

def to_float01(img):
    return img.astype(np.float32) / 255.0


def mse_metric(original, corrupted):
    a = to_float01(original)
    b = to_float01(corrupted)
    return float(np.mean((a - b) ** 2))

def mae_metric(original, corrupted):
    a = to_float01(original)
    b = to_float01(corrupted)
    return float(np.mean(np.abs(a - b)))

def rmse_metric(original, corrupted):
    return float(np.sqrt(mse_metric(original, corrupted)))


def psnr_metric(original, corrupted, eps=1e-12):
    mse = mse_metric(original, corrupted)

    if mse < eps:
        return float("inf")

    return float(10 * np.log10(1.0 / mse))
    
def ssim_metric(original, corrupted):
    original_f = to_float01(original)
    corrupted_f = to_float01(corrupted)

    return float(
        compare_ssim(
            original_f,
            corrupted_f,
            channel_axis=2,
            data_range=1.0
        )
    )

def gray_uint8(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


def laplacian_variance_metric(img):
    gray = gray_uint8(img)
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    return float(lap.var())


def tenengrad_metric(img):
    gray = gray_uint8(img)
    gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize = 3)
    gy - cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize = 3)
    ten = gx ** 2 + gy ** 2 
    return float(np.mean(ten))



def brightness_metric(img):
    gray = gray_uint8(img).astype(np.float32) / 255.0
    return float(np.mean(gray))


def entropy_metric(img, bins=256):
    gray = gray_uint8(img).astype(np.float32) / 255.0

    hist, _ = np.histogram(
        gray,
        bins=bins,
        range=(0,1)
    )

p = hist.astype(np.float32)
p = p / (p.sum() + 1e-12)
p = p[p > 0]

return float(-np.sum(p * np.log2(p)))

def compute_standard_metrics(original, corrupted):
    lap_orig = laplacian_variance_metric(original)
    lap_corr = laplacian_variance_metric(corrupted)

    ten_orig = tenengrad_metric(original)
    ten_corr = tenengrad_metric(corrupted)

    return {
        "mse": mse_metric(original, corrupted),
        "mae": mae_metric(original, corrupted),
        "rmse": rmse_metric(original, corrupted),
        "psnr": psnr_metric(original, corrupted),
        "ssim": ssim_metric(original, corrupted),

        "laplacian_original": lap_orig,
        "laplacian_corrupted": lap_corr,
        "laplacian_ratio": float(
            lap_corr / (lap_orig + 1e-12)
        ),

        "tenengrad_original": ten_orig,
        "tenengrad_corrupted": ten_corr,
        "tenengrad_ratio": float(
            ten_corr / (ten_orig + 1e-12)
        ),

        "brightness_original": brightness_metric(original),
        "brightness_corrupted": brightness_metric(corrupted),

        "contrast_original": contrast_metric(original),
        "conotrast_corrupted": contrast_metric(corrupted),

        "entropy_original": entropy_metric(original),
        "entropy_corrupted": entropy_metric(corrupted),
    }