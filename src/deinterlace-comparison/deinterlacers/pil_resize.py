import numpy as np
from PIL import Image


class PillowNearest:
    kind = Image.NEAREST
    name = f'PIL Nearest'

    shape = '*'
    facecolor = None

    def deinterlace(self, image, interlacing_factor=2, axis=0):
        dim = list(image.shape)
        for i in range(image.ndim):
            dim[i] = dim[i] * (interlacing_factor if axis == i else 1)

        pil_im = Image.fromarray(image)

        out_im = pil_im.resize(dim, self.kind)

        return np.array(out_im)


class PillowLinear(PillowNearest):
    kind = Image.BILINEAR
    name = f'PIL bilinear'

    shape = '*'
    facecolor = 'w'


class PillowBox(PillowNearest):
    kind = Image.BOX
    name = f'PIL box'

    shape = '*'
    facecolor = 'w'


class PillowHamming(PillowNearest):
    kind = Image.HAMMING
    name = f'PIL hamming'

    shape = '*'
    facecolor = None


class PillowBicubic(PillowNearest):
    kind = Image.BICUBIC
    name = f'PIL bicubic'

    shape = '*'
    facecolor = 'w'


class PillowLanczos(PillowNearest):
    kind = Image.LANCZOS
    name = f'PIL lanczos'

    shape = '*'
    facecolor = 'w'
