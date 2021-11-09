import numpy as np

class NumPy_Bilinear_v1:

    name = "NumPy Bilinear v1"

    def deinterlace(self, image, interlacing_factor, axis=0):
        output = np.repeat(image, interlacing_factor, axis=axis)

        output[1:-1:2, :] = (output[1:-1:2, :] + output[2::2, :]) / 2
        return output