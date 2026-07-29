ARTIFACT_CONFIG = {
    "seed": 42,
    "resize_to": (256, 256),
    "severity_levels": [
        "mild",
        "moderate",
        "severe",
    ],
    "focus_blur": {
        "blur_scale": 0.8,
        "mild": {"sigma_range": [0.6, 1.2]},
        "moderate": {"sigma_range": [1.3, 2.3]},
        "severe": {"sigma_range": [2.4, 4.0]},
    },

    "brightness_contrast": {
        "mild": {
            "brightness_delta_range": [0.03, 0.10],
            "contrast_delta_range": [0.03, 0.10]
        }
    },

    "dark_spots": {
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
            "edge_softness_range": [0.5, 1.1 ]
        },

        "severe": {
            "num_spots_range": [6, 9],
            "radius_range": [12, 27],
            "opacity_range": [0.45, 0.90],
            "edge_softness_range": [0.7, 1.3]
        }
    },

    "jpeg_compression": {
        "mild": {"quality_range": [85, 95]},
        "moderate": {"quality_range": [55, 80]},
        "severe": {"quality_range": [20, 50]}
    },

    "stain_variation": {
        "mild": {
            "strength": [0.25, 0.45],
            "contrast_delta_range": [0.03, 0.10],
            "value_delta_range": [0.03, 0.8]
        },

        "moderate": { 
            "strength": [0.45, 0.75],
            "contrast_delta_range": [0.10, 0.25],
            "value_delta_range": [0.08, 0.16]
        },

        "severe": {
            "strength": [0.75, 1.10],
            "contrast_delta_range": [0.25, 0.50],
            "value_delta_range": [0.16, 0.30]
        },

        "schemes": [
            "balanced",
            "hematoxylin_like",
            "eosin_like",
            "pale",
            "overstained",
            "cool_shift",
            "warm_shift"
        ]
    }
}