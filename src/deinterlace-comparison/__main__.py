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
# to open the data (if .tif) and for output
import tifffile as tf
# used to load in all the deinterlacing modules
from load_modules import load_deinterlace_modules
# takes the input and removes half the lines :)
from interlace import interlace
# gets the quality of the di
from quality_measure import image_similarity
# for example image
from scipy.misc import face as sci_face

# the file you want to interlace then deinterlace!
input_file_path = 'test.dm4'

# how many times to run reconstruction for timing average
n_time_averaging = 1000

# look in 'quality_measure.py' for this
image_difference_measure = 'root_mean_square_error'

output_folder = 'plot_outputs'

# make a folder for output
if not os.path.exists('outputs'):
    os.mkdir('outputs')

output_path = os.path.join('outputs', output_folder)

if not os.path.exists(output_path):
    os.mkdir(output_path)

# read in the file
# filename can be full path, otherwise looks in current working directory
file_ext = os.path.splitext(input_file_path)[1]
image = None  # just to suppress some lint warnings
if file_ext in ['.dm3', '.dm4']:
    dmf = DM3(input_file_path)
    # extract the actual image as a numpy array
    # NOTE: working with 32-bit images for the OpenCV stuff
    image = dmf.image.astype(np.float32)
elif file_ext == 'tif':
    image = tf.imread(input_file_path).astype(np.float32)
else:
    print('Error: Unsupported input file type: ' + file_ext)
    exit(1)

# image = sci_face().astype(np.float32)
# image = 0.2989 * image[:,:,0] + 0.5870 * image[:,:,1] + 0.1140 * image[:,:,2]
# sz = 512
# ih = int((image.shape[0] - sz) / 2)
# iw = int((image.shape[1] - sz) / 2)
# image = image[ih:ih+sz, iw:iw+sz]

# if 3d, just use top slice
if image.ndim == 3:
    image = image[:, :, 0]

# save original as read
tf.imwrite(os.path.join(output_path, 'original.tif'), image)

# interlace the image
image_interlaced = interlace(image)

# save interlaced
tf.imwrite(os.path.join(output_path, 'interlaced.tif'), image_interlaced)

# Load all the modules we made to do the deinterlacing
# these must be a class that contains a name member and deinterlace method

modules_path = os.path.dirname(sys.argv[0])
name = 'deinterlacers'

modules = load_deinterlace_modules(name, modules_path)

# now loop through out modules and test them!

di_names = []
di_times = []
di_quality = []

di_diff_profile = []
di_shp = []
di_fcol = []

# in case we want to try every 3 lines later
interlace_n = 2
# crop off edges, particularly for comparison's sake
crp = 3


for m in modules:
    # do the deinterlacing n times and time it

    di_start_time = time.perf_counter()

    di_image = None
    for i in range(n_time_averaging):
        di_image = m.deinterlace(image_interlaced, interlace_n)

    di_finish_time = time.perf_counter()
    di_elapsed_time = di_finish_time - di_start_time
    di_elapsed_time_per = di_elapsed_time / n_time_averaging

    # for odd interlacing, because of loss of decimal?
    di_image = di_image[:image.shape[0], :image.shape[1]].astype(np.float32)

    tf.imwrite(os.path.join(output_path, f'{m.name}.tif'), di_image)

    di_image_crop = di_image[crp:-crp, crp:-crp]
    ref_image = image[crp:-crp, crp:-crp]

    # get quality of deinterlacing
    di_qual = image_similarity(ref_image, di_image_crop, method=image_difference_measure, interlace_n=interlace_n)

    # save all this for plotting later
    di_names.append(m.name)
    di_times.append(di_elapsed_time_per)
    di_quality.append(di_qual)

    di_fcol.append(m.facecolor)
    di_shp.append(m.shape)

    # plot things as we go! (In a one horse open sleigh)
    print(f'Plotting difference')
    plot_image_difference(ref_image, di_image_crop, m.name, show=False, save_path=output_path)
    print(f'Done with {m.name}')

plot_time_quality_graph(di_names, di_times, di_quality, di_fcol, di_shp, n_time_averaging, show=True)






