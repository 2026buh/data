import cv2
import numpy as np

class FocusBlur:
    DEFAULT_CONFIG = {
        "blur_scale": 0.8,

        "severity_probabilities": {
            "mild": 1 / 3
            "moderate": 1 / 3
            "severe": 1 / 3
        },

        "mild": {
            "sigma_range": [0.6, 1.2]
        },

        "moderate": {
            "sigma_range": [1.3, 2.3]
        },

        "severe": {
            "sigma_range": [2.4, 4.0]
        }
    }

    VALID_SEVERITIES = [
        "mild",
        "moderate",
        "severe"
    ]

    def __init__(
        self, 
        severity="random",
        seed=42,
        config=None
    ):
        self.config = (
            config
            if config is not None
            else self.DEFAULT_CONFIG
        )

        self.severity = severity
        self.rng = np.random.default_rng(seed)

        valid_options = ["random"] + self.VALID_SEVERITIES

        if self.severity not in valid_options:
            raise ValueError(
                f"severity must be one of {valid_options}"
            )

    def apply(self, image):

        if self.severity == "random":
            probabilities = self.config[
                "severity_probabilities"
            ]

            selected_severity = str(
                self.rng.choice(
                    self.VALID_SEVERITIES,
                    p=[
                        probabilities["mild"],
                        probabilities["moderate"],
                        probabilities["severe"]
                    ]
                )
            )

        else:
            selected_severity = self.severity

        sigma_range = self.config[
            selected_severity
        ]["sigma_range"]

        sampled_sigma = float(
            self.rng.uniform(*sigma_range)
        )

        blur_scale = float(
            self.config.get("blur_scale", 1.0)
        )

        final_sigma = sampled_sigma * blur_scale

        blurred_image = cv2.GaussianBlur(
            image,
            ksize=(0, 0),
            sigmaX=final_sigma,
            sigmaY=final_sigma
        )

        metadata = {
            "artifact": "focus_blur",
            "severity": selected_severity,
            "sampled_sigma": sampled_sigma,
            "blur_scale": blur_scale,
            "final_sigma": final_sigma
        }

        return blurred_image, metadata