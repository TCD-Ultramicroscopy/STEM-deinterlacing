import diplib
import numpy as np


class diplib_resample_nearest:
    name = "DIPlib Resampling Nearest"
    method = 'nearest'

    shape = 's'
    markercolor = 'C3'
    facecolor = 'w'

    def deinterlace(self, image, interlacing_factor, axis=0):
        scale = [1, 1]
        scale[axis - 1] = 2

        # also a parameter for shift=(0,0) - I guess it shifts the image as well, but not entirely sure.
        deint = np.array(diplib.Resampling(image, scale, interpolationMethod=self.method))

        return deint


class diplib_resample_inversenearest(diplib_resample_nearest):
    name = "DIPlib Resampling Inverse Nearest"
    method = 'inverse nearest'

    markercolor = 'C2'


class diplib_resample_linear(diplib_resample_nearest):
    name = "DIPlib Resampling Linear"
    method = 'linear'

    markercolor = 'C1'


class diplib_resample_3cubic:
    name = "DIPlib Resampling 3 Cubic"

    method = '3-cubic'

    markercolor = 'C0'


class diplib_resample_4cubic(diplib_resample_nearest):
    name = "DIPlib Resampling 4 Cubic"
    method = '4-cubic'

    markercolor = 'C4'


class diplib_resample_ft(diplib_resample_nearest):
    name = "DIPlib Resampling Ft"
    method = 'ft'

    markercolor = 'C5'


class diplib_resample_lanczos2(diplib_resample_nearest):
    name = "DIPlib Resampling Lanczos 2"
    method = 'lanczos2'

    markercolor = 'C6'

class diplib_resample_lanczos3(diplib_resample_nearest):
    name = "DIPlib Resampling Lanczos 3"
    method = 'lanczos3'

    markercolor = 'C7'

class diplib_resample_lanczos4(diplib_resample_nearest):
    name = "DIPlib Resampling Lanczos 4"
    method = 'lanczos4'

    markercolor = 'C8'

class diplib_resample_lanczos6(diplib_resample_nearest):
    name = "DIPlib Resampling Lanczos 6"
    method = 'lanczos6'

    markercolor = 'C9'

class diplib_resample_lanczos8(diplib_resample_nearest):
    name = "DIPlib Resampling Lanczos 8"
    method = 'lanczos8'

    markercolor = '#E4AC9E'