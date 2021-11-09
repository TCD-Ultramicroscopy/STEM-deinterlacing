import cv2
import numpy as np

class OpenCV_IP_NS:
    radius = 1

    name = f"OpenCV Inpaint NS (r={radius})"

    def deinterlace(self, image, interlacing_factor=2, axis=0):
        dim = list(image.shape)
        for i in range(image.ndim):
            dim[i] = dim[i] * (interlacing_factor if axis == i else 1)

        image_full = np.zeros(dim, dtype=image.dtype)
        image_mask = np.zeros(dim, dtype=np.uint8)
        image_full[::2, :] = image
        image_mask[1::2, :] = 1

        return cv2.inpaint(image_full, image_mask, self.radius, cv2.INPAINT_NS)

class OpenCV_IP_NS_r5(OpenCV_IP_NS):
    radius = 5

    name = f"OpenCV Inpaint NS (r={radius})"