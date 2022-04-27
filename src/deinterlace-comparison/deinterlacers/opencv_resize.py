import cv2


class OpenCV_Nearest:
    name = "OpenCV Nearest"

    shape = 'o'
    facecolor = 'C3'

    def deinterlace(self, image, interlacing_factor=2, axis=0):
        dim = list(image.shape)
        for i in range(image.ndim):
            dim[i] = dim[i] * (interlacing_factor if axis == i else 1)

        dim_xy = (dim[1], dim[0])
        return cv2.resize(image, dim_xy, interpolation=cv2.INTER_NEAREST)


class OpenCV_Area:
    name = "OpenCV Area"

    shape = 'o'
    facecolor = None

    def deinterlace(self, image, interlacing_factor=2, axis=0):
        dim = list(image.shape)
        for i in range(image.ndim):
            dim[i] = dim[i] * (interlacing_factor if axis == i else 1)

        dim_xy = (dim[1], dim[0])
        return cv2.resize(image, dim_xy, interpolation=cv2.INTER_AREA)


class OpenCV_Bilinear:
    name = "OpenCV Bilinear"

    shape = 's'
    facecolor = 'w'

    def deinterlace(self, image, interlacing_factor=2, axis=0):
        dim = list(image.shape)
        for i in range(image.ndim):
            dim[i] = dim[i] * (interlacing_factor if axis == i else 1)

        dim_xy = (dim[1], dim[0])

        return cv2.resize(image, dim_xy, interpolation=cv2.INTER_LINEAR)



class OpenCV_Bicubic:
    name = "OpenCV Bicubic"

    shape = 's'
    facecolor = 'w'

    def deinterlace(self, image, interlacing_factor=2, axis=0):
        dim = list(image.shape)
        for i in range(image.ndim):
            dim[i] = dim[i] * (interlacing_factor if axis == i else 1)

        dim_xy = (dim[1], dim[0])
        return cv2.resize(image, dim_xy, interpolation=cv2.INTER_CUBIC)


class OpenCV_Lanczos:
    name = "OpenCV Lanczos"

    shape = 's'
    facecolor = 'w'

    def deinterlace(self, image, interlacing_factor=2, axis=0):
        dim = list(image.shape)
        for i in range(image.ndim):
            dim[i] = dim[i] * (interlacing_factor if axis == i else 1)

        dim_xy = (dim[1], dim[0])
        return cv2.resize(image, dim_xy, interpolation=cv2.INTER_LANCZOS4)