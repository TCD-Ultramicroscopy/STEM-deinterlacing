# main script to compare deinterlacing
from compare_deinterlacers import compare_deinterlacers
# for example image
from scipy.misc import face as sci_face


# the file you want to interlace then deinterlace!
input = 'test.dm4'

# optional load in test image from scipy
# input = sci_face().astype(np.float32)
# input = 0.2989 * image[:,:,0] + 0.5870 * image[:,:,1] + 0.1140 * image[:,:,2]
# sz = 512
# ih = int((input.shape[0] - sz) / 2)
# iw = int((input.shape[1] - sz) / 2)
# input = input[ih:ih+sz, iw:iw+sz]

# how many times to run reconstruction for timing average
n_time_averaging = 1000

# look in 'quality_measure.py' for this
image_difference_measure = 'root_mean_square_error'

# this is the folder for the outputs
output_folder = 'plot_outputs'

compare_deinterlacers(input, n_time_averaging, image_difference_measure, output_folder)