import cv2

# NOTE: This does something that is not a strict bilinear interpolation
# see here: https://stackoverflow.com/questions/43598373/opencv-resize-result-is-wrong

class OpenCV_Bilinear:
    name = "OpenCV Bilinear"

    def deinterlace(self, image, interlacing_factor=2, axis=0):
        dim = list(image.shape)
        for i in range(image.ndim):
            dim[i] = dim[i] * (interlacing_factor if axis == i else 1)

        return cv2.resize(image, tuple(dim), interpolation=cv2.INTER_LINEAR)