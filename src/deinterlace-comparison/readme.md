# STEM deinterlacer comparison

## About

This folder contains python scripts to interlace an input image, deinterlace it and compare to the ground truth. The script is run through ``__main__.py``, where there are also some configuration settings.

## Deinterlacers

Deinterlacing algorithms can be found in the ``deinterlacers`` folder. The scripts will search this folder for any valid class that will perform the deinterlacing.

The following is the basic format of the class

```python
import numpy as np

# class name chould be unique
class NumPy_Repeat:

    # the name that appears on plot outputs
    name = "NumPy Repeat"

    # style for plotting
    shape = 'o'
    markercolor = 'C3'
    facecolor = None

    # function that returns the deinterlaced images.
    # Output must be the same shape as the ground truth image.
    def deinterlace(self, image, interlacing_factor, axis=0):
        return np.repeat(image, interlacing_factor, axis=axis)
```