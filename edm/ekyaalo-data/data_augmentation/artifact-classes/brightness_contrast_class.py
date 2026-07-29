import numpy as np

class BrightnessContrast:
    DEFAULT_CONFIG = {
        "severity_probabilities": {
            "mild": 1 / 3,
            "moderate": 1 / 3,
            "severe": 1 / 3
        },

        "mild": {
            "brightness_delta_range": [0.03, 0.10],
            "contrast_delta_range": [0.03, 0.10]
        },

        "moderate": {
            "brightness_delta_range": [0.10, 0.22],
            "contrast_delta_range": [ 0.10. 0.25]
        },

        "severe": {
            "brightness_delta_range": [0.22, 0.40],
            "contrast_delta_range": [0.25, 0.50]
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

    def _random_signed_factor(self, delta_range):

        delta = float(
            self.rng.uniform(*delta_range)
        )

        sign = float(
            self.rng.choice([-1, 1])
        )

        return 1.0 + sign * delta 

        @staticmethod
        def _clip_uint8(image):
            return np.clip(
                image, 
                0,
                255
            ).astype(np.uint8)

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

            severity_config = self.config[
                selected_severity
            ]

            brightness_factor = self._random_signed_factor(
                severity_config["brightness_delta_range"]
            )

            contrast_factor = self._random_signed_factor(
                severity_config["brightness_delta_range"]
            )

            contrast_factor = self._random_signed_factor(
                severity_config["contrast_delta_range"]
            )

            adjusted_image = image.astype(np.float32)

            adjusted_image *= brightness_factor

            mean = np.mean(
                adjusted_image,
                axis=(0, 1),
                keepdims=True
            )

            adjusted_image = (
                adjusted_image - mean
            ) * contrast_factor + mean

            adjusted_image = self._clip_uint8(
                adjusted_image
            )

            metadata = {
                "artifact": "brightness_contrast",
                "severity": selected_severity,
                "brightness_factor": brightness_factor,
                "contrast_factor": contrast_factor
            }

            return adjusted_image, metadata