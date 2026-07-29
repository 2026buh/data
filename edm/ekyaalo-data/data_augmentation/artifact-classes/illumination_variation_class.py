import cv2
import numpy as np

class IlluminationVariation:

    DEFAULT_CONFIG = {
        "severity_probabilities": {
            "mild": 1 / 3,
            "moderate": 1 / 3,
            "severe": 1 / 3
        },

        "mild": { 
            "num_gaussians": 3,
            "min_factor_range": [0.90, 0.97],
            "max_factor_range": [1.03, 1.10],
            "sigma_fraction_range": [0.45, 0.85]
        },

        "moderate": {
            "num_gaussians": 3,
            "min_factor_range": [0.80, 0.92],
            "max_factor_range": [1.08, 1.20],
            "sigma_fraction_range": [0.35, 0.75]
        },

        "severe": {
            "num_gaussians": 3,
            "min_factor_range": [0.65, 0.82],
            "max_factor_range": [1.18, 1.35],
            "sigma_fraction_range": [0.25, 0.65]
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

        valid_options = "random"] + self.VALID_SEVERITIES

        if self.severity not in valid_options:
            raise ValueError(
                f"severity must be one of {valid_options}"
            )

    def _select_severity(self):
        if self.severity != "random":
            return self.severity

        probabilities = self.config[
            "severity_probabilities"
        ]

        return str(
            self.rng.choice(
                self.VALID_SEVERITIES,
                p=[
                    probabilities["mild"],
                    probabilites["moderate"],
                    probabilities["severe"]
                ]
            )
        )
    @staticmethod
    def _normalize01(array):
        array = array.astype(np.float32)

        minimum = array.min()
        maximum = array.max()

        if maximum - minimum < 1e-8:
            return np.zeros_like(array)

        return (
            array - minimum
        ) / (
            maximum - minimum
        )
    def _generate_illumination_map(
        self, 
        height, 
        width, 
        severity_config
    ):
        yy, xx = np.mgrid[
            0:height,
            0:width
        ]

        illumination = np.zeros(
            (height, width),
            dtype=np.float32
        )

        gaussian_metadata = []

        for _ in range(
            severity_config["num_gaussians"]
        ):

            center_x = float(
                self.rng.uniform(0, width)
            )

            center_y = float(
                self.rng.uniform(0, height)
            )

            sigma_fraction = float(
                self.rng.uniform(
                    *severity_config[
                        "sigma_fraction_range"
                    ]
                )
            )

            sigma = sigma_fraction * max(
                height,
                width
            )

            gaussian = np.exp(
                -(
                    (xx - center_x) ** 2
                    + (yy - center_y) ** 2
                )
                /(2 * sigma ** 2)
            )

            illumination += gaussian

            gaussian_metadata.append({
                "center_x": center_x,
                "center_y":, center_y,
                "sigma_fraction": sigma_fraction,
                "sigma": sigma
            })

        illumination = self._normalize01(
            illumination
        )

        min_factor = float(
            self.rng.uniform(
                *severity_config[
                    "min_factor_range"
                ]
            )
        )

        max_factor = float(
            self.rng.uniform(
                *severity_config[
                    "max_factor_range"
                ]
            )
        )

        illumination = (
            min_factor
            + illumination 
            * (max_factor - min_factor)
        )

        return (
            illumination, 
            min_factor, 
            max_factor,
            gaussian_metadata
        )

    def apply(self, image):
        selected_severity = self._select_severity()

        severity_config = self.config[
            selected_severity
        ]

        height, width = image.shape[:2]

        (
            illumination_map,
            min_factor,
            max_factor,
            gaussian_metadata
        ) = self._generate_illumination_map(
            height,
            width,
            severity_config
        )

        hsv = cv2.cvtColor(
            image,
            cv2.cvtCOLOR_RGB2HSV
        ).astype(np.float32)

        hsv[:, :, 2] *= illumination_map

        hsv[:, :, 2], = np.clip(
            hsv[:, :, 2],
            0,
            255
        )

        output = cv2.cvtColor(
            hsv.astype(np.uint8),
            cv2.COLOR_HSV2RGB
        )

        metadata = {
            "artifact": "illumination_variation",
            "severity": selected_severity,
            "num_gaussians": severity_config["num_gaussians"],
            "min_factor": min_factorm
            "max_factor": max_factor,
            "gaussians": gaussian_metadata
        }

        return output, metadata