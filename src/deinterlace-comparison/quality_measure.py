import numpy as np
from skimage.metrics import structural_similarity, peak_signal_noise_ratio, normalized_root_mse
from scipy.signal import fftconvolve
from scipy.signal import medfilt

from cv2 import PSNR
import matplotlib.pyplot as plt


def image_similarity(image_reference, image_2, method='root_mean_square_error', interlace_n=2):
    # im_ref = image_reference[:-(interlace_n-1), interlace_n:-interlace_n]
    # im_2 = image_2[:-(interlace_n-1), interlace_n:-interlace_n]

    im_ref = image_reference
    im_2 = image_2

    if method == 'root_mean_square_error':
        return _root_mean_square_error(im_ref, im_2)
    elif method == 'structural_similarity':
        return _structural_similarity(im_ref, im_2)
    elif method == 'cross_correlation':
        return _cross_correlation(im_ref, im_2)
    elif method == 'fft_diff_var':
        return _fft_diff_var(im_ref, im_2)
    else:
        print("Not a valid image similarity measurment")
        return 0.0


def _root_mean_square_error(image_reference, image_2):
    image_ref_range = np.max(image_reference) - np.min(image_reference)
    mse = np.sum(np.power(image_reference-image_2, 2)) / image_reference.size
    return np.sqrt(mse) / image_ref_range


def _structural_similarity(image_reference, image_2):
    return structural_similarity(image_reference, image_2)


def _cross_correlation(image_reference, image_2):
    corr = fftconvolve(image_reference, image_2, mode='same')

    return np.max(corr)


def _fft_diff_var(image_reference, image_2):
    diff = image_2 - image_reference
    diff_fft = np.fft.fftshift(np.fft.fft2(diff))

    ny, nx = image_reference.shape

    mid_y = int(np.floor(ny / 2))
    mid_x = int(np.floor(nx / 2))

    diff_fft[:mid_y, :] = 0

    diff_fft[mid_y, :mid_x] = 0

    diff_fft_sum = np.sum(diff_fft)

    return np.abs(diff_fft_sum)


def _fft_diff_var_3(image_reference, image_2):
    diff = image_2 - image_reference
    diff_fft = np.fft.fftshift(np.fft.fft2(diff))
    diff_fft = np.abs(diff_fft)

    profile = np.mean(diff_fft, axis=1)

    return np.mean(np.abs(np.gradient(profile)))


def _fft_diff_var_2(image_reference, image_2):
    diff = image_2 - image_reference
    diff_fft = np.fft.fftshift(np.fft.fft2(diff))
    diff_fft = np.abs(diff_fft)

    bac = np.median(np.abs(np.fft.fftshift(np.fft.fft2(image_reference))))

    mse = np.sum(np.power(diff_fft - bac, 2)) / image_reference.size

    return mse

