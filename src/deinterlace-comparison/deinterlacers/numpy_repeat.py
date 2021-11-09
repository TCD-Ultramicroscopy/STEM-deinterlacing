import numpy as np

class NumPy_Repeat:

    name = "NumPy Repeat"

    def deinterlace(self, image, interlacing_factor, axis=0):
        return np.repeat(image, interlacing_factor, axis=axis)