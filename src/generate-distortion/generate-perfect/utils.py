###############################################################################
#
# utils.py
#
# Created by Jonathan J. P. Peters
#
# Utilities for generating a STEM-like image, mostly maths/geometry
#
###############################################################################

import numpy as np
import scipy.interpolate as sci_interp
import matplotlib.pyplot as plt

#
# The sublattice class is a convenient way to store the peak data
#
class Sublattice:
    def __init__(self, origin, fwhm, amplitude, scale):
        self.origin = np.array(origin)
        self.fwhm = fwhm / scale
        self.amplitude = amplitude

        self.px_rad = int(self.fwhm * 2)
        sz = 51
        inc = self.px_rad * 2 / sz
        self.y = np.linspace(-self.px_rad, self.px_rad, num=sz, endpoint=True)
        self.x = np.linspace(-self.px_rad, self.px_rad, num=sz, endpoint=True)
        xv, yv = np.meshgrid(self.x, self.y)
        self.z = self.gauss(xv, yv, self.fwhm, self.amplitude)

        self.interp = sci_interp.RectBivariateSpline(self.x, self.y, self.z)

    def gauss(self, _x, _y, _fwhm, _amp):

        x2 = np.power(_x, 2)
        y2 = np.power(_y, 2)

        g = _amp * np.exp(-4 * np.log(2) * (x2 + y2) / (_fwhm * _fwhm))
        return np.swapaxes(g, 0, 1)

    def eval(self, pos_int, pos_f):

        x_i = np.arange(-self.px_rad, self.px_rad + 1)
        y_i = np.arange(-self.px_rad, self.px_rad + 1)

        im = self.interp(y_i - pos_f[0], x_i - pos_f[1])

        x_i += pos_int[1]
        y_i += pos_int[0]

        return x_i, y_i, im


def generate_rotation_matrix(rotation_deg):
    rotation_rad = np.deg2rad(rotation_deg)
    rotation_mat = np.array([[np.cos(rotation_rad), -np.sin(rotation_rad)],
                             [np.sin(rotation_rad), np.cos(rotation_rad)]])
    return rotation_mat


#
# This uses affine transformation to calculate how much we need to tile
# the a and b vecs to cover a square area (image_size)
#
def calculate_tiling(image_size, a_vec, b_vec, rotation_mat, scale):

    a_vec = np.matmul(rotation_mat, a_vec)
    b_vec = np.matmul(rotation_mat, b_vec)

    orig_basis = np.array([[1, 1, 1], [0, a_vec[0], b_vec[0]], [0, a_vec[1], b_vec[1]]])

    new_basis = np.array([[0, 1, 0], [0, 0, 1]])

    transform_mat = np.matmul(new_basis, np.linalg.inv(orig_basis))

    # this is the 4 corners of the image
    image_basis = np.array([[1.0, 1.0, 1.0, 1.0], [0, image_size[1], 0, image_size[1]], [0, 0, image_size[0], image_size[0]]])
    image_basis[1:, 1] *= scale
    image_basis[1:, 2] *= scale

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

    return x_tile_min, x_tile_max, y_tile_min, y_tile_max
