###############################################################################
#
# __main__.py
#
# Created by Jonathan J. P. Peters
#
# This script defines a few variables, then calls the main body of the code.
#
###############################################################################

# main script to compare deinterlacing
from compare_deinterlacers import compare_deinterlacers
# for example image
import numpy as np
from scipy.misc import face as sci_face

# the filepath of the dm3/dm4/tif file you want to interlace then deinterlace!
#
# input_file = 'test.dm4'

# input_file can also be a numpy array!
# load in test image from scipy
#
input_file = sci_face().astype(np.float32)
input_file = 0.2989 * input_file[:,:,0] + 0.5870 * input_file[:,:,1] + 0.1140 * input_file[:,:,2]
sz = 512
ih = int((input_file.shape[0] - sz) / 2)
iw = int((input_file.shape[1] - sz) / 2)
input_file = input_file[ih:ih+sz, iw:iw+sz]

# how many times to run reconstruction for timing average
#
n_time_averaging = 1

# look in 'quality_measure.py' for this
#
image_difference_measure = 'root_mean_square_error'

# this is the folder for the outputs (will make this folder inside an 'outputs' folder)
#
output_folder = 'plot_outputs_test'

# This is where the magic happens
#
return_vals = compare_deinterlacers(input_file, n_time_averaging, image_difference_measure, output_folder)

    
