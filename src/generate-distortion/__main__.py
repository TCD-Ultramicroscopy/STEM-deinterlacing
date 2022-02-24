import numpy as np
import tifffile
import os
import shutil
import inspect

from generate_distortions import get_distortions, normalise_amp

from distort_image import distort_image


def deinterlace(image, interlacing_factor, axis=0):
    output = np.repeat(image, interlacing_factor, axis=axis)

    output[1:-1:2, :] = (output[1:-1:2, :] + output[2::2, :]) / 2
    return output

#
# Define input variables
#

# time variables of acquisition
dose = 100  # electrons per microsecond
flyback_time = 500  # us
dwell_times = [40, 1, 20, 10, 8, 5, 4, 2]  # us
num_frames = [1, 40, 2, 4, 5, 8, 10, 20]

# distortion frequency information
reuse_waves = True
# These are only used when generating outputs
freq_range = (0.1, 75)  # min, max
n_freq = 100
amp_range = (1 / n_freq, 10 / n_freq)  # min, max (px)
# amp_range = (10 / n_freq, 50 / n_freq)  # min, max (px)
#drift_vec = np.array([2.8, 3.6])  # px per s
drift_vec = np.array([0.0, 0.0])  # px per s

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

output_dir_base = "output"
i = 0
output_dir = f'{output_dir_base}_{i}'
while os.path.exists(output_dir):
    i += 1
    output_dir = f'{output_dir_base}_{i}'

print(f'Output directory: {output_dir}')

if not os.path.exists(output_dir):
    os.mkdir(output_dir)

shutil.copy("generate-perfect/perfect.tif", os.path.join(output_dir, "perfect.tif"))
in_image = tifffile.imread("generate-perfect/perfect.tif")
# in_image = in_image[::2, ::2]
out_size = (512, 512)  # crop image to avoid ege artefacts from distortion shifts
# out_size = (np.array(in_image.shape) / 2).astype(np.int32)

# Let's Go!

waves_info = get_distortions(n_freq=n_freq, freq_range=freq_range, amp_range=amp_range, reuse=reuse_waves)
waves = waves_info['waves']

# save the waves to our output folder
shutil.copy("waves.pickle", os.path.join(output_dir, "waves.pickle"))

# lets just save some parameters in case we want to revisit this
with open(os.path.join(output_dir, "parameters.txt"), 'w') as f:
    f.write(f'dose: {dose}\n')
    f.write(f'flyback: {flyback_time}\n')
    f.write(f'n_freq: {waves_info["n_freq"]}\n')
    f.write(f'freq_range: {waves_info["freq_range"]}\n')
    f.write(f'amp_range: {waves_info["amp_range"]}\n')
    f.write(f'drift_vec: {(drift_vec[0], drift_vec[1])}\n')

    f.write(f'amp_norm_func:\n{inspect.getsource(normalise_amp)}\n')

for do_int in [True, False]:
    for do_rot in [False, True]:
        for dt, nf in zip(dwell_times, num_frames):
            if do_int:
                nf *= 2

            out_images, out_dist_x, out_dist_y = distort_image(in_image, out_size, waves, dt, flyback_time, nf, drift_vec,
                                                               interlace=do_int, dose=dose, do_rotation=do_rot,
                                                               plot_outputs=plot_outputs)

            out_stack = np.zeros((nf, out_size[0], out_size[0]), dtype=np.float64)

            for i in range(nf):
                if do_int:
                    if do_rot:
                        ax = i % 2
                    else:
                        ax = 0
                    out_stack[i, ...] = deinterlace(out_images[i], 2, axis=ax)
                else:
                    out_stack[i, ...] = out_images[i]

            folder_name = ''
            if do_int:
                folder_name += 'int'
            else:
                folder_name += 'full'

            if do_rot:
                folder_name += '_rot'

            if not os.path.exists(os.path.join(output_dir, folder_name)):
                os.mkdir(os.path.join(output_dir, folder_name))

            dt_str = f'{dt}'.replace('.', '-')

            with open(os.path.join(os.path.join(output_dir, folder_name), f"image_nf_{nf:03}_dt_{dt_str}.npy"), "wb") as f:
                np.save(f, out_stack)
