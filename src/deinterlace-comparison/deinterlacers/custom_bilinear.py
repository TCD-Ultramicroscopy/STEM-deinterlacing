import numpy as np

class CustomBilinear:

    name = "Custom Bilinear v1"

    def deinterlace(self, image, interlacing_factor, axis=0):
        output = np.repeat(image, interlacing_factor, axis=axis)

        output[1:-1:2, :] *= 0.2

        output[1:-1:2, :] += output[2::2, :] * 0.2

        # top right
        output[1::2, 0:-1] += output[0::2, 1:] * 0.1

        # top left
        output[1::2, 1:] += output[0::2, 0:-1] * 0.1

        # bottom right
        output[1:-1:2, 0:-1] += output[2::2, 1:] * 0.1

        # bottom left
        output[1:-1:2, 1:] += output[2:-1:2, 0:-1] * 0.1


        # top right right
        output[1::2, 0:-2] += output[0::2, 2:] * 0.05

        # top left left
        output[1::2, 2:] += output[0::2, 0:-2] * 0.05


        # bottom right right
        output[1:-1:2, 0:-2] += output[2::2, 2:] * 0.05

        # bottom left left
        output[1:-1:2, 2:] += output[2:-1:2, 0:-2] * 0.05

        return output

class Lewys_Custom_2:

    name = "The Lewys Special v2"

    def deinterlace(self, image, interlacing_factor, axis=0):
        output = np.repeat(image, interlacing_factor, axis=axis)

        output[1:-1:2, :] *= 0.3

        output[1:-1:2, :] += output[2::2, :] * 0.3

        # top right
        output[1::2, 0:-1] += output[0::2, 1:] * 0.15

        # top left
        output[1::2, 1:] += output[0::2, 0:-1] * 0.15

        # bottom right
        output[1:-1:2, 0:-1] += output[2::2, 1:] * 0.15

        # bottom left
        output[1:-1:2, 1:] += output[2:-1:2, 0:-1] * 0.15


        # top right right
        output[1::2, 0:-2] += output[0::2, 2:] * -0.05

        # top left left
        output[1::2, 2:] += output[0::2, 0:-2] * -0.05


        # bottom right right
        output[1:-1:2, 0:-2] += output[2::2, 2:] * -0.05

        # bottom left left
        output[1:-1:2, 2:] += output[2:-1:2, 0:-2] * -0.05

        return output