import cv2

class ImageLoader:
    def __init__(
        self,
        resize=None,
        interpolation=cv2.INTER_AREA
    ):

        self.resize = resize
        self.interpolation = interpolation
    def load(self, image_path):

        image = cv2.imread(image_path)

        if image is None:
            raise FileNotFoundError(
                f"Could not load image: {image_path}"
            )
        
        image = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )

        if self.resize is not None:
            image = cv2.resize(
                image, 
                self.resize,
                interpolation=self.interpolation
            )
        return image
    def save(self, image, output_path):
        image = cv2.cvtColor(
            image,
            cvv2.COLOR_RGB2BGR
        )

        success = cv2.imwrite(
            output_path,
            image
        )

        if not success:
            raise RuntimeError(
                f"Could not save image: {output_path}"
            )
