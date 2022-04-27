import diplib
import numpy as np

class diplib_resample_3cubic:

    name = "diplib 3-cubic"

    method = '3-cubic'

    shape = 'D'
    facecolor = None

    def deinterlace(self, image, interlacing_factor, axis=0):
        scale = [1, 1]
        scale[axis - 1] = 2

        # also a parameter for shift=(0,0) - I guess it shifts the image as well, but not entirely sure.

        deint = np.array(diplib.Resampling(image, scale, interpolationMethod=self.method))

        return deint

class diplib_resample_4cubic(diplib_resample_3cubic):
    name = "diplib 4-cubic"
    method = '4-cubic'

class diplib_resample_linear(diplib_resample_3cubic):
    name = "diplib linear"
    method = 'linear'

class diplib_resample_nearest(diplib_resample_3cubic):
    name = "diplib nearest"
    method = 'nearest'

class diplib_resample_inversenearest(diplib_resample_3cubic):
    name = "diplib inverse nearest"
    method = 'inverse nearest'

class diplib_resample_bspline(diplib_resample_3cubic):
    name = "diplib bspline"
    method = 'bspline'

class diplib_resample_lanczos8(diplib_resample_3cubic):
    name = "diplib lanczos8"
    method = 'lanczos8'

class diplib_resample_lanczos6(diplib_resample_3cubic):
    name = "diplib lanczos6"
    method = 'lanczos6'
    shape = 'P'

class diplib_resample_lanczos4(diplib_resample_3cubic):
    name = "diplib lanczos4"
    method = 'lanczos4'
    shape = 'P'

class diplib_resample_lanczos3(diplib_resample_3cubic):
    name = "diplib lanczos3"
    method = 'lanczos3'
    shape = 'P'

class diplib_resample_lanczos2(diplib_resample_3cubic):
    name = "diplib lanczos2"
    method = 'lanczos2'
    shape = 'P'

class diplib_resample_ft(diplib_resample_3cubic):
    name = "diplib ft"
    method = 'ft'
    shape = 'P'