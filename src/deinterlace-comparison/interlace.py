###############################################################################
#
# interlace.py
#
# Created by Jonathan J. P. Peters
#
# A simple function to take an image and interlace it.
#
###############################################################################

import numpy as np

def interlace(data, axis=0, skip_n=2, offset=0):
	offset = offset % skip_n
	indices = np.arange(offset, data.shape[axis], skip_n)

	return np.take(data, indices, axis=axis)