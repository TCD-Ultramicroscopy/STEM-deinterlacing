###############################################################################
#
# generate_perfect.py
#
# Created by Jonathan J. P. Peters
#
# This script generates a STEM-like image to avoid the need of simulation when
# doing simple testing.
#
###############################################################################

import numpy as np
import matplotlib.pyplot as plt
import tifffile
from scipy.ndimage import rotate as scipy_rot
from utils import Sublattice, calculate_tiling, generate_rotation_matrix

# output image size
image_size = np.array([1024, 1024])

scale = 1.0  # Angstroms per pixel
# separate y scale is not supported

# Structure is defined using two lattice vectors and relative sublattice vectors
# with an intesity and FWHM

#
# STO 100
#

# the two lattice vectors
a_vec = np.array([4.0, 0.0])  # Angstrom
b_vec = np.array([0.0, 4.0])  # Angstrom

# the atom positions within the unite cell (in Angstroms
sublattices = [Sublattice([0.0, 0.0], 1.2, 0.8, scale),
               Sublattice([2.0, 2.0], 1.2, 0.3, scale)]

#
# Si 110
#

# # the two lattice vectors
# a_vec = np.array([4.16, 0.0])  # Angstrom
# b_vec = np.array([0.0, 5.62])  # Angstrom
#
# # the atom positions within the unit cell (in Angstroms), fwhm and amplitude
# sublattices = [Sublattice([0.0, 0.0], 0.8, 0.8, scale),
#                Sublattice([0.0, 1.36], 0.8, 0.8, scale),
#                Sublattice([2.08, 2.81], 0.8, 0.8, scale),
#                Sublattice([2.08, 4.17], 0.8, 0.8, scale)
#                ]

# # rotation of the image
# rotation = -47.2  # degrees
rotation = 72  # degrees

# background intensity
baseline = 0.1

# generate rotation matrix to use in a couple of places
rotation_mat = generate_rotation_matrix(rotation)

# Use affine transforms to calculate how much we need to tile our basis
x_tile_min, x_tile_max, y_tile_min, y_tile_max = calculate_tiling(image_size, a_vec, b_vec, rotation_mat, scale)

#
# Do the tiling
#

out_image = np.zeros(image_size)
out_image += baseline

for i in range(x_tile_min, x_tile_max + 1):
    for j in range(y_tile_min, y_tile_max + 1):

        # the current coord of the unit cell
        coord = i * a_vec + j * b_vec

        for sl in sublattices:
            cd = (np.matmul(rotation_mat, sl.origin + coord)) / scale

            if np.any(cd < -sl.px_rad) or np.any(cd > image_size + sl.px_rad):
                continue

            cd_i = cd.astype(np.int64)  # y, x
            cd_f = cd - cd_i  # y, x

            # cd_f *= np.array([-1.0, 1.0])

            xx, yy, vv = sl.eval(cd_i, cd_f)

            val_x = np.logical_and(xx >= 0, xx < image_size[1])
            xx = xx[val_x]

            val_y = np.logical_and(yy >= 0, yy < image_size[0])
            yy = yy[val_y]

            vv = vv[np.ix_(val_y, val_x)]

            if vv.size == 0 or vv.shape[0] == 0 or vv.shape[1] == 0:
                continue

            out_image[np.ix_(yy, xx)] += vv



plt.imshow(out_image, origin='lower')
plt.show()

tifffile.imwrite("perfect.tif", out_image.astype(np.float32))


print("Beep boop. All done!")

