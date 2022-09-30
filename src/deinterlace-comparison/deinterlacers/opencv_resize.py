import cv2


class OpenCV_Nearest:
    name = "OpenCV Resize Nearest"

    shape = 'o'
    markercolor = 'C3'
    facecolor = 'w'

    kind = cv2.INTER_NEAREST

    def deinterlace(self, image, interlacing_factor=2, axis=0):
        dim = list(image.shape)
        for i in range(image.ndim):
            dim[i] = dim[i] * (interlacing_factor if axis == i else 1)

        dim_xy = (dim[1], dim[0])
        return cv2.resize(image, dim_xy, interpolation=self.kind)


class OpenCV_Area(OpenCV_Nearest):
    name = "OpenCV Resize Area"

    markercolor = 'C2'

    kind = cv2.INTER_AREA


class OpenCV_Bilinear(OpenCV_Nearest):
    name = "OpenCV Resize Bilinear"

    markercolor = 'C1'

    kind = cv2.INTER_LINEAR


class OpenCV_Bicubic(OpenCV_Nearest):
    name = "OpenCV Resize Bicubic"

    markercolor = 'C0'

    kind = cv2.INTER_CUBIC


class OpenCV_Lanczos(OpenCV_Nearest):
    name = "OpenCV Resize Lanczos"

    markercolor = 'C4'

    kind = cv2.INTER_LANCZOS4
