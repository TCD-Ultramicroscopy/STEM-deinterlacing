import numpy as np

class CustomBilinear:

    name = "Custom Bilinear v1"

    shape = '^'
    markercolor = 'C3'
    facecolor = 'w'

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

class Custom_2:

    name = "Custom Bilinear v2"

    shape = '^'
    markercolor = 'C2'
    facecolor = 'w'

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


class NumPy_C_Bilinear_v1:

    name = "Custom Bilinear v3"

    shape = '^'
    markercolor = 'C1'
    facecolor = 'w'

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


class NumPy_C_Bilinear_v2:

    name = "Custom Bilinear v4"

    shape = '^'
    markercolor = 'C0'
    facecolor = 'w'

    def deinterlace(self, image, interlacing_factor, axis=0):
        output = np.repeat(image, interlacing_factor, axis=axis)

        f = interlacing_factor

        for i in range(1, f):
            # top
            output[i::f, :] *= 0.6 * (f-i) / f

            # bottom
            output[i:-f+1:f, :] += 0.6 * output[f::f, :] * i / f

            diag_r = np.sqrt(2 * f**2)
            r_top = np.sqrt(2 * i**2)
            r_bottom = np.sqrt(2 * (f-i)**2)

            # top right
            output[i::f, :-i] += 0.2 * output[0::f, i:] * r_bottom / diag_r

            # top left
            output[i::f, (f-i):] += 0.2 * output[0::f, :-(f-i)] * r_bottom / diag_r

            # bottom right
            output[i:-f+1:f, :-i] += 0.2 * output[f::f, i:] * r_top / diag_r

            # bottom left
            output[i:-f+1:f, (f-i):] += 0.2 * output[f::f, :-(f-i)] * r_top / diag_r

        return output