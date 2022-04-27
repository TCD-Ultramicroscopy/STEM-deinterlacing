import numpy as np
import scipy.signal as sp_signal

class scipy_resample_default:

    name = "SciPy resample (default)"

    shape = '3'
    facecolor = None

    def deinterlace(self, image, interlacing_factor, axis=0):
        dim = list(image.shape)
        for i in range(image.ndim):
            dim[i] = dim[i] * (interlacing_factor if axis == i else 1)

        n_samples = dim[axis]

        return sp_signal.resample(image, n_samples)

class scipy_resample_boxcar:

    name = "SciPy resample boxcar"

    shape = '3'
    facecolor = None

    window_str = 'boxcar'

    def deinterlace(self, image, interlacing_factor, axis=0):
        dim = list(image.shape)

        old_samples = dim[axis]

        for i in range(image.ndim):
            dim[i] = dim[i] * (interlacing_factor if axis == i else 1)

        new_samples = dim[axis]

        window = sp_signal.get_window(self.window_str, old_samples)

        deint = sp_signal.resample(image, new_samples, axis=axis, window=window)
        return deint


#
# Warning, these are largely useless
#

# class scipy_resample_triang(scipy_resample_boxcar):
#     name = "SciPy resample triang"
#     window_str = 'triang'


# class scipy_resample_blackman(scipy_resample_boxcar):
#     name = "SciPy resample blackman"
#     window_str = 'blackman'


# class scipy_resample_hamming(scipy_resample_boxcar):
#     name = "SciPy resample hamming"
#     window_str = 'hamming'


# class scipy_resample_hann(scipy_resample_boxcar):
#     name = "SciPy resample hann"
#     window_str = 'hann'


# class scipy_resample_bartlett(scipy_resample_boxcar):
#     name = "SciPy resample bartlett"
#     window_str = 'bartlett'


# class scipy_resample_flattop(scipy_resample_boxcar):
#     name = "SciPy resample flattop"
#     window_str = 'flattop'


# class scipy_resample_parzen(scipy_resample_boxcar):
#     name = "SciPy resample parzen"
#     window_str = 'parzen'


# class scipy_resample_bohman(scipy_resample_boxcar):
#     name = "SciPy resample bohman"
#     window_str = 'bohman'


# class scipy_resample_blackmanharris(scipy_resample_boxcar):
#     name = "SciPy resample blackmanharris"
#     window_str = 'blackmanharris'


# class scipy_resample_nuttall(scipy_resample_boxcar):
#     name = "SciPy resample nuttall"
#     window_str = 'nuttall'


# class scipy_resample_barthann(scipy_resample_boxcar):
#     name = "SciPy resample barthann"
#     window_str = 'barthann'


# class scipy_resample_cosine(scipy_resample_boxcar):
#     name = "SciPy resample cosine"
#     window_str = 'cosine'