import cv2
import numpy as np

class DarkSpots:

    DEFAULT_CONFIG = {
        "severity_probabilities": {
            "mild": 1 / 3,
            "moderate": 1 / 3,
            "severe": 1 / 3
        },

        "mild": {
            "num_spots_range": [1, 3],
            "radius_range": [4, 12],
            "opacity_range": [0.30, 0.45],
            "edge_softness_range": [0.4, 0.9]
        },

        "moderate": {
            "num_spots_range": [3, 7],
            "radius_range": [8, 22],
            "opacity_range": [0.40, 0.55],
            "edge_softness_range": [0.5, 1.1]
        },

        "severe": {
            "num_spots_range": [6, 9],
            "radius_range": [12, 27],
            "opacity_range": [0.45, 0.90],
            "edge_softness_range": [0.7, 0.9]
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
                    probabilities["moderate"],
                    probabilities["severe"]
                ]
            )
        )
    
    @staticmethod
    def _normalize01(array):
        array = array.astype(np.float32)

        minimum = array.min()
        maximum = array.max()

        if maximum - minimum < 1e -8:
            return np.zeros_like(array)

        return (
            array - minimum
        ) / (
            maximum - minimum
        )
        
    def apply(self, image):
        selected_severity = self._select_severity()

        severity_config = self.config [
            selected_severity
        ]

        height, width = image.shape[:2]

        output = image.astype(
            np.float32
        ).copy()

        yy, xx = np.mgrid[
            0:height,
            0:width
        ]

        minimum_spots, maximum_spots = (
            severity_config["num_spots_range"]
        )

        num_spots = int(
            self.rng.integers(
                minimum_spots,
                maximum_spots + 1
            )
        )

        spot_metadata = []
        for _ in range(num_spots):
            radius = float(
                self.rng.uniform(
                    *severity_config["radius_range"]
                )
            )

            opacity = float(
                self.rng.uniform(
                    *severity_config["opacity_range"]
                )
            )

            softness = float(
                self.rng.uniform(
                    *severity_config[
                        "edge_softness_range"
                    ]
                )
            )

            center_x = float(
                self.rng.uniform(
                    -radius,
                    width + radius
                )
            )

            center_y = float(
                self.rng.uniform(
                    -radius,
                    height + radius
                )
            )

            distance = np.sqrt(
                (xx - center_x) ** 2
                +(yy - center_y) ** 2
            )

            sigma = radius * softness

            mask = np.exp(
                -(distance ** 2)
                / (2 * sigma ** 2)
            )

            mask_power = float(
                self.rng.uniform(
                    0.8,
                    1.4
                )
            )

            mask = mask ** mask_power
            mask = np.clip(mask, 0, 1)

            noise = self.rng.normal(
                0,
                1,
                size=(height, width)
            ).astype(np.float32)

            noise = self._normalize01(noise)
            
            noise_sigma = max(
                radius * 0.45,
                2
            )

            noise = cv2.GaussianBlur(
                noise,
                ksize=(0, 0),
                sigmaX=noise_sigma,
                sigmaY=noise_sigma
            )

            irregularity_strength = float(
                self.rng.uniform(
                    0.05, 
                    0.20
                )
            )

            mask = mask * (
                1.0 
                - irregularity_strength 
                + irregularity_strength * noise
            )

            mask = np.clip(mask, 0, 1)

            spot_value = float(
                self.rng.uniform(
                    0, 18
                )
            )

            spot_color = np.array(
                [
                    spot_value,
                    spot_value,
                    spot_value
                ],
                dtype=np.float32
            )

            alpha = (
                opacity 
                * mask[:, :, None]
            )

            output = (
                output * (1 - alpha)
                + spot_color * alpha
            )

            spot_metadata.append({
                "radius": radius,
                "opacity": opacity,
                "softness": softness, 
                "center_x": center_x,
                "center_y": center_y,
                "mask_power": mask_power,
                "irregularity_strength": irregularity_strength,
                "spot_value": spot_value
            })
        
        output = np.clip(
            output, 0,
            255
        ).astype(np.uint8)

        metadata = {
            "artifact": "dark_spots",
            "severity": selected_severity,
            "num_spots": num_spots,
            "spots": spot_metadata
        }

        return output, metadata