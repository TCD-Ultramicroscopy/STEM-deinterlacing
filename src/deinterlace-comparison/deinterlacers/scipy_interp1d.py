import numpy as np
from scipy.interpolate import interp1d


class ScipyNearest:
    kind = 'nearest'
    name = f'SciPy Interp 1D Nearest'

    shape = 'D'
    markercolor = 'C3'
    facecolor = 'w'

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
    name = f'SciPy Interp 1D Linear'

    markercolor = 'C2'


class ScipySlinear(ScipyNearest):
    kind = 'slinear'
    name = f'SciPy Interp 1D Slinear'

    markercolor = 'C1'


class ScipyZero(ScipyNearest):
    kind = 'zero'
    name = f'SciPy Interp 1D Zero'

    markercolor = 'C0'


class ScipyQuadratic(ScipyNearest):
    kind = 'quadratic'
    name = f'SciPy Interp 1D Quadratic'

    markercolor = 'C4'


class ScipyCubic(ScipyNearest):
    kind = 'cubic'
    name = f'SciPy Interp 1D Cubic'

    markercolor = 'C5'
