import numpy as np
import tifffile
import os

from generate_distortions import get_distortions

from distort_image import distort_image

#
# Define input variables
#

# time variables of acquisition
dose = 100  # electrons per microsecond
flyback_time = 500  # us
dwell_times = [40, 1, 20, 10, 8, 5, 4, 2]  # us
num_frames = [1, 40, 2, 4, 5, 8, 10, 20]
do_rotation = False
interlace = False

# distortion frequency information
freq_range = (0.1, 75)  # min, max
n_freq = 100
amp_range = (1 / n_freq, 5 / n_freq)  # min, max (px)
# amp_range = (10 / n_freq, 50 / n_freq)  # min, max (px)
drift_vec = np.array([2.8, 3.6])  # px per s

plot_outputs = False

# Set image to process

# # this is just a test image
# from scipy import misc
# in_image = misc.face().astype(np.float64)
# in_image = np.dot(in_image[..., :3], [0.2989, 0.5870, 0.1140])  # convert to greyscale
# in_image = in_image - np.min(in_image)
# in_image = in_image / np.max(in_image)
# in_image = in_image + 1
# out_size = (256, 256)

in_image = tifffile.imread("generate-perfect/perfect.tif")
# in_image = in_image[::2, ::2]
out_size = (512, 512)  # crop image to avoid ege artefacts from distortion shifts
# out_size = (np.array(in_image.shape) / 2).astype(np.int32)

# Let's Go!

waves = get_distortions(n_freq=n_freq, freq_range=freq_range, amp_range=amp_range, reuse=True, save=True)

for dt, nf in zip(dwell_times, num_frames):
    out_images, out_dist_x, out_dist_y = distort_image(in_image, out_size, waves, dt, flyback_time, nf, drift_vec,
                                                       interlace=interlace, dose=dose, do_rotation=do_rotation,
                                                       plot_outputs=plot_outputs)

    out_stack = np.zeros((nf, out_images[0].shape[0], out_images[0].shape[1]), dtype=np.float64)

    for i in range(nf):
        out_stack[i, ...] = out_images[i]

    if not os.path.exists('output'):
        os.mkdir('output')

    dt_str = f'{dt}'.replace('.', '-')

    with open(os.path.join('output', f"image_nf_{nf:03}_dt_{dt_str}.npy"), "wb") as f:
        np.save(f, out_stack)
