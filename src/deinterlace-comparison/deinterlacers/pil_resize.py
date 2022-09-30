import numpy as np
from PIL import Image


class PillowNearest:
    kind = Image.NEAREST
    name = f'PIL Resize Nearest'

    shape = 's'
    markercolor = 'C3'
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
    name = f'PIL Resize Bilinear'

    markercolor = 'C2'


class PillowBox(PillowNearest):
    kind = Image.BOX
    name = f'PIL Resize Box'

    markercolor = 'C1'


class PillowHamming(PillowNearest):
    kind = Image.HAMMING
    name = f'PIL Resize Hamming'

    markercolor = 'C0'


class PillowBicubic(PillowNearest):
    kind = Image.BICUBIC
    name = f'PIL Resize Bicubic'

    markercolor = 'C4'


class PillowLanczos(PillowNearest):
    kind = Image.LANCZOS
    name = f'PIL Resize Lanczos'

    markercolor = 'C5'
