import numpy as np
from scipy.interpolate import interp1d


class ScipyNearest:
    kind = 'nearest'
    name = f'Scipy interp1d {kind}'

    shape = 'o'
    facecolor = '#ffff00'

    def deinterlace(self, image, interlacing_factor=2, axis=0):
        dim = list(image.shape)
        for i in range(image.ndim):
            dim[i] = dim[i] * (interlacing_factor if axis == i else 1)

        current_points = np.linspace(0, image.shape[axis], image.shape[axis], endpoint=False)
        new_points = np.linspace(0, image.shape[axis], dim[axis], endpoint=False)
        new_points[-interlacing_factor+1:] = new_points[-interlacing_factor]  # accounts for final value falling outside interpolation range

        f = interp1d(current_points, image, axis=axis, kind=self.kind)

        return f(new_points)


class ScipyLinear(ScipyNearest):
    kind = 'linear'
    name = f'Scipy interp1d {kind}'

    shape = 'o'
    # facecolor = 'w'


class ScipySlinear(ScipyNearest):
    kind = 'slinear'
    name = f'Scipy interp1d {kind}'

    shape = 'o'
    # facecolor = 'w'


class ScipyZero(ScipyNearest):
    kind = 'zero'
    name = f'Scipy interp1d {kind}'

    shape = 'o'
    # facecolor = None


class ScipyQuadratic(ScipyNearest):
    kind = 'quadratic'
    name = f'Scipy interp1d {kind}'

    shape = 'o'
    # facecolor = 'w'


class ScipyCubic(ScipyNearest):
    kind = 'cubic'
    name = f'Scipy interp1d {kind}'

    shape = 'o'
    # facecolor = 'w'
