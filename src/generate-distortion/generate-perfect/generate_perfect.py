import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as sci_interp
import tifffile

image_size = np.array([1024, 1024])

scale_x = 0.2  # Angstroms per pixel
scale_y = scale_x  # separate y scale is not supported

a_vec = np.array([4.0, 0.0])  # Angstrom
b_vec = np.array([0.0, 4.0])  # Angstrom

rotation = -7.2  # degrees

baseline = 0.1

class Sublattice:
    def __init__(self, origin, fwhm, amplitude):
        self.origin = np.array(origin)
        self.fwhm = fwhm / scale_x
        self.amplitude = amplitude

        self.px_rad = int(self.fwhm * 2)
        sz = 50
        inc = self.px_rad * 2 / sz
        self.y = np.arange(-self.px_rad, self.px_rad + inc, inc)
        self.x = np.arange(-self.px_rad, self.px_rad + inc, inc)
        xv, yv = np.meshgrid(self.x, self.y)
        self.z = self.gauss(xv, yv, self.fwhm, self.amplitude)

        self.interp = sci_interp.RectBivariateSpline(self.x, self.y, self.z)

    def gauss(self, _x, _y, _fwhm, _amp):

        x2 = np.power(_x, 2)
        y2 = np.power(_y, 2)

        return _amp * np.exp(-4 * np.log(2) * (x2 + y2) / (_fwhm * _fwhm))

    def eval(self, pos_int, pos_f):

        x_i = np.arange(-self.px_rad, self.px_rad + 1)
        y_i = np.arange(-self.px_rad, self.px_rad + 1)

        im = self.interp(x_i + pos_f[1], y_i + pos_f[0])

        x_i += pos_int[1]
        y_i += pos_int[0]

        return x_i, y_i, im


sublattices = [Sublattice([0.0, 0.0], 1.2, 0.8),
               Sublattice([2.0, 2.0], 1.2, 0.3)]


#
# Use affine transforms to calculate how much we need to tile our basis
#

rotation_rad = np.deg2rad(rotation)
rotation_mat = np.array([[np.cos(rotation_rad), -np.sin(rotation_rad)], [np.sin(rotation_rad), np.cos(rotation_rad)]])

a_vec = np.matmul(rotation_mat, a_vec)
b_vec = np.matmul(rotation_mat, b_vec)

orig_basis = np.array([[1, 1, 1], [0, a_vec[0], b_vec[0]], [0, a_vec[1], b_vec[1]]])

new_basis = np.array([[0, 1, 0], [0, 0, 1]])

transform_mat = np.matmul(new_basis, np.linalg.inv(orig_basis))

# this is the 4 corners of the image
image_basis = np.array([[1.0, 1.0, 1.0, 1.0], [0, image_size[1], 0, image_size[1]], [0, 0, image_size[0], image_size[0]]])
image_basis[1:, 1] *= scale_x
image_basis[1:, 2] *= scale_y

trans_im_basis = np.matmul(transform_mat, image_basis)

x_tile_min = np.min(trans_im_basis[0, :])
x_tile_max = np.max(trans_im_basis[0, :])

y_tile_min = np.min(trans_im_basis[1, :])
y_tile_max = np.max(trans_im_basis[1, :])

x_tile_min = np.sign(x_tile_min) * np.ceil(np.abs(x_tile_min))
x_tile_max = np.sign(x_tile_max) * np.ceil(np.abs(x_tile_max))

y_tile_min = np.sign(y_tile_min) * np.ceil(np.abs(y_tile_min))
y_tile_max = np.sign(y_tile_max) * np.ceil(np.abs(y_tile_max))

x_tile_min = int(x_tile_min)
x_tile_max = int(x_tile_max)
y_tile_min = int(y_tile_min)
y_tile_max = int(y_tile_max)

#
# Do the tiling
#

out_image = np.zeros(image_size)
out_image += baseline

for i in range(x_tile_min, x_tile_max + 1):
    for j in range(y_tile_min, y_tile_max + 1):

        coord = i * a_vec + j * b_vec

        for sl in sublattices:
            cd = (coord + np.matmul(rotation_mat, sl.origin)) / scale_x

            if np.any(cd < -sl.px_rad) or np.any(cd > image_size + sl.px_rad):
                continue

            cd_i = cd.astype(np.int64)
            cd_f = cd - cd_i

            xx, yy, vv = sl.eval(cd_i, cd_f)

            val_x = np.logical_and(xx >= 0, xx < image_size[1])
            xx = xx[val_x]

            val_y = np.logical_and(yy >= 0, yy < image_size[0])
            yy = yy[val_y]

            vv = vv[np.ix_(val_y, val_x)]

            if vv.size == 0 or vv.shape[0] == 0 or vv.shape[1] == 0:
                continue

            out_image[np.ix_(yy, xx)] += vv



# plt.imshow(out_image, origin='lower')
# plt.show()

tifffile.imsave("perfect.tif", out_image.astype(np.float32))


print("boop")

