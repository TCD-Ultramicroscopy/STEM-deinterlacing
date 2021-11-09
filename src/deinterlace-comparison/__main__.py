# general stuff
import os
import sys
# for timing (no shit!)
import time
# for displaying the data
from plotting import plot_image_difference, plot_time_quality_graph
# numpy is life
import numpy as np
# to open the data (loads the local file 'read_dm3.py')
from read_dm3 import DM3
# used to load in all the deinterlacing modules
from load_modules import load_deinterlace_modules
# takes the input and removes half the lines :)
from interlace import interlace
# gets the quality of the di
from quality_measure import image_similarity

# the file you want to interlace then deinterlace!
input_file_path = 'test.dm4'

# how many times to run reconstruction for timing average
n_time_averaging = 10

# look in 'quality_measure.py' for this
image_difference_measure = 'root_mean_square_error'

# read in the file
# filename can be full path, otherwise looks in current working directory
dmf = DM3(input_file_path)

# extract the actual image as a numpy array
# NOTE: working with 32-bit images for the OpenCV stuff
image = dmf.image.astype(np.float32)

# interlace the image
image_interlaced = interlace(image)

# Load all the modules we made to do the deinterlacing
# these must be a class that contains a name member and deinterlace method

modules_path = os.path.dirname(sys.argv[0])
name = 'deinterlacers'

modules = load_deinterlace_modules(name, modules_path)

# now loop through out modules and test them!

di_names = []
di_times = []
di_quality = []

for m in modules:
    # do the deinterlacing n times and time it

    di_start_time = time.perf_counter()

    for i in range(n_time_averaging):
        di_image = m.deinterlace(image_interlaced, 2)

    di_finish_time = time.perf_counter()
    di_elapsed_time = di_finish_time - di_start_time
    di_elapsed_time_per = di_elapsed_time / n_time_averaging

    # get quality of deinterlacing
    di_qual = image_similarity(image, di_image, method=image_difference_measure)

    # save all this for plotting later
    di_names.append(m.name)
    di_times.append(di_elapsed_time_per)
    di_quality.append(di_qual)

    # plot things as we go! (In a one horse open sleigh)
    plot_image_difference(image, di_image, m.name, show=True)

plot_time_quality_graph(di_names, di_times, di_quality, n_time_averaging)






