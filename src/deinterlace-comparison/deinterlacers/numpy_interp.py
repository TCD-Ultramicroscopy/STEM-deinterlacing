import numpy as np

class NumPy_Repeat:

    name = "NumPy Repeat"

    shape = 'o'
    facecolor = None

    def deinterlace(self, image, interlacing_factor, axis=0):
        return np.repeat(image, interlacing_factor, axis=axis)

class NumPy_Bilinear_v1:

    name = "NumPy Bilinear v1"

    shape = 'o'
    facecolor = 'w'

    def deinterlace(self, image, interlacing_factor, axis=0):
        output = np.repeat(image, interlacing_factor, axis=axis)

        output[1:-1:2, :] = (output[1:-1:2, :] + output[2::2, :]) / 2
        return output