###############################################################################
#
# distort_image.py
#
# Created by Jonathan J. P. Peters
#
# This file is where the actual image distortions are applied.
#
###############################################################################

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import map_coordinates
from generate_distortions import add_noise
import tifffile
import os


def distort_image(input_image, output_size, waves, dwell_time, flyback_time, num_frames, drift_vec, interlace=False, dose=1, do_rotation=False, plot_outputs=False):

    in_image = np.copy(input_image)

    #
    # Generate some basic image indexing
    #

    # create an x, y coordinate for every pixel
    x_full = np.arange(in_image.shape[1])
    y_full = np.arange(in_image.shape[0])
    xv_full, yv_full = np.meshgrid(x_full, y_full)

    #
    # Now go through the images and generate the distortions
    #

    total_time = 0

    out_images = []
    out_dist_x = []
    out_dist_y = []

    for n in range(num_frames):

        if do_rotation:
            n_rot = n % 4  # number of 90 degree rotations
        else:
            n_rot = 0

        if n_rot % 2:
            fast_scan_dim = 0
            slow_scan_dim = 1
        else:
            fast_scan_dim = 1
            slow_scan_dim = 0

        # this is all in terms of time coordinates, not position (hence the t!)
        xt = np.arange(output_size[fast_scan_dim])
        yt = np.arange(output_size[slow_scan_dim])
        if interlace:
            yt = yt[::2] / 2
        xvt, yvt = np.meshgrid(xt, yt)

        xvt = xvt.astype(np.float64)
        yvt = yvt.astype(np.float64)

        time_image = (flyback_time + xvt * dwell_time)  # time within line
        time_image += yvt * (flyback_time + xvt.shape[1] * dwell_time)  # time within image
        time_image += total_time  # time within series

        time_image = np.rot90(time_image, -n_rot)

        # TODO: could add interframe time here
        total_time = np.max(time_image) + dwell_time

        dist_x_image = np.zeros_like(time_image, dtype=np.float64)
        dist_y_image = np.zeros_like(time_image, dtype=np.float64)

        dist_x_image += time_image * drift_vec[1] * 10**-6
        dist_y_image += time_image * drift_vec[0] * 10**-6

        # generate the full distortion field for this slice
        for w in waves:
            dists = w.gen(time_image)
            dist_x_image += dists[1]
            dist_y_image += dists[0]

        #
        # resample image
        #

        # this is where we will sample the original image at
        new_x = xv_full.astype(np.float64)
        new_y = yv_full.astype(np.float64)

        # this is now indices on the original image (without offset)
        x = np.arange(output_size[1])
        y = np.arange(output_size[0])
        if interlace:
            if n_rot % 2:
                x = x[::2]
            else:
                y = y[::2]
        xv, yv = np.meshgrid(x, y)

        margin_l = int((in_image.shape[1] - output_size[1]) / 2)
        margin_t = int((in_image.shape[0] - output_size[0]) / 2)

        if n_rot == 1:
            margin_l += 1
        elif n_rot == 2:
            margin_t += 1

        xv += margin_l
        yv += margin_t

        new_x[yv, xv] += dist_x_image
        new_y[yv, xv] += dist_y_image

        out_image = map_coordinates(in_image, (new_y, new_x))
        out_image = out_image[margin_t:margin_t+output_size[0], margin_l:margin_l+output_size[1]]

        in_image_crop = in_image[margin_t:margin_t+output_size[0], margin_l:margin_l+output_size[1]]

        if interlace:
            if n_rot % 2:
                in_image_crop = in_image_crop[:, ::2]
                out_image = out_image[:, ::2]
            else:
                in_image_crop = in_image_crop[::2, :]
                out_image = out_image[::2, :]

        out_image = add_noise(out_image, dose, dwell_time)

        out_images.append(out_image)
        out_dist_x.append(dist_x_image)
        out_dist_y.append(dist_y_image)

        # #
        # # save output data
        # #
        #
        # # if not os.path.exists('output'):
        # #     os.mkdir('output')
        # #
        # # out_path = os.path.join('output', f'frames_{nf}_dt_{dt}')
        # #
        # # if not os.path.exists(out_path):
        # #     os.mkdir(out_path)
        # #
        # # tifffile.imsave(os.path.join(out_path, f"output_{n:03}.tif"), out_image.astype(np.float32))
        # #
        # # tifffile.imsave(os.path.join(out_path, f"dist_x_{n:03}.tif"), dist_x_image.astype(np.float32))
        # # tifffile.imsave(os.path.join(out_path, f"dist_y_{n:03}.tif"), dist_y_image.astype(np.float32))
        #
        # #
        # # plot data
        # #

        if plot_outputs:
            fig, axs = plt.subplots(2, 2)

            axs[0, 0].set_title("Original image")
            axs[0, 0].imshow(in_image_crop, cmap='gray')

            axs[0, 1].set_title("Corrupted image")
            axs[0, 1].imshow(out_image, cmap='gray')

            axs[1, 0].set_title("x distortion")
            axs[1, 0].imshow(dist_x_image, cmap='gray')

            axs[1, 1].set_title("y distortion")
            axs[1, 1].imshow(dist_y_image, cmap='gray')

            for ax in axs.flat:
                ax.set_axis_off()

            plt.show()

    return out_images, out_dist_x, out_dist_y

    #
    # Boom!
    #
