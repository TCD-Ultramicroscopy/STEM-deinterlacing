import numpy as np


class FFT_spline:

    name = "FFT spline"

    shape = 's'
    facecolor = None

    def deinterlace(self, image, interlacing_factor, axis=0):
        dim = list(image.shape)
        for i in range(image.ndim):
            dim[i] = dim[i] * (interlacing_factor if axis == i else 1)

        image_full = np.zeros(dim, dtype=image.dtype)
        image_full[::interlacing_factor, :] = image

        # take fft
        fft = np.fft.fft2(image_full)

        y_d = int(dim[0] / (interlacing_factor * 2))
        x_d = int(dim[1] / (interlacing_factor * 2))

        fft[y_d:-y_d, :] = 0.0

        # think factor of two comes from missing half of pixels
        out = np.real(np.fft.ifft2(fft)) * interlacing_factor

        return out


class FFT_spline_smooth_v1:

    sigma = 0

    name = f"FFT spline, sigma = {sigma}"

    shape = 's'
    facecolor = None

    def deinterlace(self, image, interlacing_factor, axis=0):
        dim = list(image.shape)
        for i in range(image.ndim):
            dim[i] = dim[i] * (interlacing_factor if axis == i else 1)

        image_full = np.zeros(dim, dtype=image.dtype)
        image_full[::interlacing_factor, :] = image

        # take fft
        fft = np.fft.fft2(image_full)

        # create mask profile

        mask_x = np.arange(dim[0]) - dim[0] / 2
        mask_x = np.fft.fftshift(mask_x)
        center = dim[0] / (interlacing_factor * 2)

        # mask_profile[np.abs(mask_x) < center] = 1
        if self.sigma == 0:
            mask_profile = np.abs(mask_x) < center
        else:
            edge_1 = center - self.sigma
            edge_0 = center + self.sigma
            mask_profile = np.clip((np.abs(mask_x) - edge_0) / (edge_1 - edge_0), 0.0, 1.0)
            mask_profile = mask_profile * mask_profile * (3 - 2 * mask_profile)

        norm_factor = dim[0] / np.sum(mask_profile)

        fft = fft * mask_profile[:, np.newaxis]

        # think factor of two comes from missing half of pixels
        out = np.real(np.fft.ifft2(fft)) * norm_factor

        return out


class FFT_spline_smooth_v1_25(FFT_spline_smooth_v1):
    sigma = 25
    name = f"FFT spline, sigma = {sigma}"


class FFT_spline_smooth_v1_50(FFT_spline_smooth_v1):
    sigma = 50
    name = f"FFT spline, sigma = {sigma}"


class FFT_spline_smooth_v2:

    sigma = 0

    name = f"FFT spline v2, sigma = {sigma}"

    shape = 's'
    facecolor = None

    def deinterlace(self, image, interlacing_factor, axis=0):
        dim = list(image.shape)
        for i in range(image.ndim):
            dim[i] = dim[i] * (interlacing_factor if axis == i else 1)

        image_full = np.zeros(dim, dtype=image.dtype)
        image_full[::interlacing_factor, :] = image

        # take fft
        fft = np.fft.fft2(image_full)

        # create mask profile

        mask_x = np.arange(dim[0]) - dim[0] / 2
        mask_x = np.fft.fftshift(mask_x)
        center = dim[0] / (interlacing_factor * 2)

        # mask_profile[np.abs(mask_x) < center] = 1
        if self.sigma == 0:
            mask_profile = np.abs(mask_x) < center
        else:
            edge_1 = center - self.sigma
            edge_0 = center + self.sigma
            mask_profile = np.clip((np.abs(mask_x) - edge_0) / (edge_1 - edge_0), 0.0, 1.0)
            mask_profile = mask_profile * mask_profile * mask_profile * (mask_profile * (6 * mask_profile - 15) + 10)

        norm_factor = dim[0] / np.sum(mask_profile)

        fft = fft * mask_profile[:, np.newaxis]

        # think factor of two comes from missing half of pixels
        out = np.real(np.fft.ifft2(fft)) * norm_factor

        return out


class FFT_spline_smooth_v2_25(FFT_spline_smooth_v2):
    sigma = 25
    name = f"FFT spline v2, sigma = {sigma}"


class FFT_spline_smooth_v2_50(FFT_spline_smooth_v2):
    sigma = 50
    name = f"FFT spline v2, sigma = {sigma}"