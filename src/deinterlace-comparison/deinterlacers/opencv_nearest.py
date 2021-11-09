import cv2

class OpenCV_Nearest:
    name = "OpenCV Nearest"

    def deinterlace(self, image, interlacing_factor=2, axis=0):
        dim = list(image.shape)
        for i in range(image.ndim):
            dim[i] = dim[i] * (interlacing_factor if axis == i else 1)
            
        return cv2.resize(image, tuple(dim), interpolation=cv2.INTER_NEAREST)