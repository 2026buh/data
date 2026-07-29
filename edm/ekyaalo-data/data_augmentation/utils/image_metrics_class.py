import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio
from skimage.metrics import structural_similarity

class ImageMetrics:
    
    def __init__(self, data_range=255):
        self.data_range = data_range

    def compute(self, reference_image, test_image):

        mse = np.mean(
            (reference_image.astype(np.float32) -
            test_image.astype(np.float32)) ** 2
        )

        psnr = peak_signal_noise_ratio(
            reference_image,
            test_image,
            data_range=self.data_range
        )

        ssim = structural_similarity(
            reference_image,
            test_image,
            channel_axis=2,
            data_range=self.data_range
        )

        laplacian_reference = cv2.Laplacian(
            reference_image,
            cv2.CV_64F
        )

        laplacian_test = cv2.Laplacian(
            test_image,
            cv2.CV_64F
        )

        sharpness_reference = np.var(
            laplacian_reference
        )

        sharpness_test = np.var(
            laplacian_test
        )

        sharpness_retention = (
            sharpness_test / 
            (sharpness_reference + 1e-8)
        ) * 100

        return { 
            "mse": float(mse),
            "psnr": float(psnr),
            "ssim": float(ssim),
            "reference_sharpness": float(sharpness_reference),
            "test_sharpness": float(
                sharpness_test
            ),
            "sharpness_retention": float(
                sharpness_retention
            )
        }