from pathlib import Path

import cv2
import numpy as np
import pandas as pd

try:
    from cellSAM import cellsam_pipeline
except ImportError as error:
    raise ImportError(
        "CellSAM is not installed. install it with: \n"
        "pip install git+https://github.com/vanvalenlab/cellSAM.git"
    ) from error

class CellSAMProcessor:

    DEFAULT_CONFIG ={
        "chunks": 256,
        "model_path": None
        "bbox_threshold": 0.4,
        "low_contrast_enhancement": False,
        "swap_channels": False,
        "use_wsi": False,
        "guage_cell_size": False,
        "block_size": 400,
        "overlap": 56,
        "iou_depth": 56,
        "iou_threshold": 0.5
    }

    def __init__(self, config=None):
        self.config = {
            **self.DEFAULT_CONFIG,
            **(config or {})
        }

        
    def prepare_image(self, image):
        if not isinstance(image, np.ndarray):
            raise TypeError(
                "image must be a NumPy array"
            )

        if image.ndim == 2:
            return image

        if image.ndim != 3:
            raise ValueError(
                "image must be a 2D grayscale image or a 3D image with 1 or 3 channels"
            )

        if image.shape[2] not in (1, 3):
            raise ValueError(
                "3D images must have either 1 or 3 channels"
            )

        return image

    def segment(self, image):

        prepared_image = self.prepare_image(image)

        mask = cellsam_pipeline(
            prepared_image,
            chunks=self.config["chunks"],
            model_path=self.config["bbox_threshold"],
            low_contrast_enhancement=(self.config["low_contrast_enhancement"]
            ),
            swap_channels=self.config["swap_channels"],
            use_wsi=self.config["use_wsi"],
            guage_cell_size=self.config["guage_cell"size"],
            block_size=self.config["block_size"],
            overlap=self.config["overlap"],
            iou_depth=self.config["iou_depth"],
            iou_threshold=self.config["iou_threshold"]

        )

        mask = np.array(
            mask,
            dtype=np.uint32
        )

        unique_labels = np.unique(mask)

        num_instances = int(
            np.count_nonzero(unique_labels)
        )

        metadata = {
            "processor": "cellsam",
            "input_shape": tuple(image.shape),
            "mask_shape": tuple(mask.shape),
            "num_instances": num_instances,
            "bbox_threshold": self.config["bbox_threshold"],
            "use_wsi": self.config["use_wsi"]
        }

        return mask, metadata

    def segment_path(self, image_path):
        image_path = Path(image_path)

        image_bgr = cv2.imread(
            str(image_path),
            cv2.IMREAD_UNCHANGED
        )

        if image_bgr is None:
            raise FileNotfoundError(
                f"Could not load image: {image_path}"
            )

        if image_bgr.ndim ==3:
            if image_bgr.shape[2] == 4:
                image_bgr = cv2.cvtColor(
                    image_bgr,
                    cv2.Color_BGRA2BGR
                )

            image = cv2.cvtColor(
                image_bgr,
                cv2.COLOR_BGR2RGB
            )
        else:
            image = image_bgr
        
        return self.segment(image)
    def save_mask(self, mask, output_path):
        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )