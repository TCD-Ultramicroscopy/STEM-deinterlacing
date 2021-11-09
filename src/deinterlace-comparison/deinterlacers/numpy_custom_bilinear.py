import numpy as np

class NumPy_C_Bilinear_v1:

    name = "NumPy Custom Bilinear v1"

    def deinterlace(self, image, interlacing_factor, axis=0):
        output = np.repeat(image, interlacing_factor, axis=axis)

        output[1:-1:2, :] *= 0.3

        output[1:-1:2, :] += output[2::2, :] * 0.3

        # top right
        output[1::2, 0:-1] += output[0::2, 1:] * 0.1

        # top left
        output[1::2, 1:] += output[0::2, 0:-1] * 0.1

        # bottom right
        output[1:-1:2, 0:-1] += output[2::2, 1:] * 0.1

        # bottom left
        output[1:-1:2, 1:] += output[2:-1:2, 0:-1] * 0.1
        return output