from __future__ import division
import numpy as np
from scipy.signal import convolve2d


class GPA:

    def __init__(self, Image):
        self.Image = Image
        self.G = None
        self.Gp = None
        self.A = None
        self.Phase = [None, None]
        self.Rot = np.array([[1, 0], [0, 1]], dtype=float)

    def getPhase(self, i, Px, Py, sig):
        if i != 0 and i != 1:
            return
        self.Phase[i] = braggPhase(self.FFT, Px, Py, sig)

    @property
    def FFT(self):
        return np.fft.fft2(self.Image)

    @property
    def PowerSpectrum(self):
        return np.fft.fftshift(np.abs(np.log(self.FFT + 1)))

    def Rotation(self, angle, unit='deg'):
        a = 0
        if unit == 'deg':
            a = angle * np.pi / 180
        else:
            a = angle

        self.Rot = np.array([[np.cos(a), np.sin(a)], [-np.sin(a), np.cos(a)]],
                            dtype=float)

    def getDisplacementField(self):
        P1 = self.Phase[0].phase
        P2 = self.Phase[1].phase

        self.G = np.array([[self.Phase[0]._Gx, self.Phase[1]._Gx],
                           [self.Phase[0]._Gy, self.Phase[1]._Gy]])
        self.A = np.linalg.inv(self.G.T)

        # Apply rotation
        # self.A = np.inner(self.A, self.Rot)

        P1 = P1 - np.round(P1 / (2 * np.pi)) * 2 * np.pi
        P2 = P2 - np.round(P2 / (2 * np.pi)) * 2 * np.pi


        self.ux = -1 / (2 * np.pi) * (self.A[0, 0] * P1 + self.A[0, 1] * P2)
        self.uy = -1 / (2 * np.pi) * (self.A[1, 0] * P1 + self.A[1, 1] * P2)

    def getStrains(self):

        self.getDisplacementField()

        d1dx, d1dy = self.Phase[0].expDifferential
        d2dx, d2dy = self.Phase[1].expDifferential

        # should replace with ddx[], ddy[]
        self.d1dx = d1dx
        self.d2dx = d2dx
        self.d1dy = d1dy
        self.d2dy = d2dy

        self.G = np.array([[self.Phase[0]._Gx, self.Phase[1]._Gx],
                           [self.Phase[0]._Gy, self.Phase[1]._Gy]])
        self.Gp = np.array([[self.Phase[0]._Gpx, self.Phase[1]._Gpx],
                            [self.Phase[0]._Gpy, self.Phase[1]._Gpy]])
        self.A = np.linalg.inv(self.G.T)  # transpose then invert

        # Apply rotation
        self.A = np.inner(self.Rot, self.A)

        # multithread?
        self.Exx = -1 / (2 * np.pi) * \
            (self.A[0, 0] * d1dx + self.A[0, 1] * d2dx)
        self.Exy = -1 / (2 * np.pi) * \
            (self.A[0, 0] * d1dy + self.A[0, 1] * d2dy)
        self.Eyx = -1 / (2 * np.pi) * \
            (self.A[1, 0] * d1dx + self.A[1, 1] * d2dx)
        self.Eyy = -1 / (2 * np.pi) * \
            (self.A[1, 0] * d1dy + self.A[1, 1] * d2dy)

        # self.getDeformationField()

    def getDeformationField(self):
        # this is eq E.4 in Martin Hytch's paper
        # REMEMBER that A * transpose (delta G) is just e (calculated above in getStrain())
        # but negative
        # Still no idea why the final -1s but they seem to make the answer not shit?

        # deformation = e + 1???

        a = 1 - self.Exx
        b = -self.Exy
        c = -self.Eyx
        d = 1 - self.Eyy
        D = a * d - b * c
        self.Exx = d / D - 1
        self.Exy = b / D
        self.Eyx = c / D
        self.Eyy = a / D - 1


class braggPhase:

    def __init__(self, FFT, Px, Py, sigma):
        self._Hg = FFT

        self.s = self._Hg.shape

        self._sigma = sigma
        self._mask = np.zeros(self.s)

        self._Px = Px
        self._Py = Py

        self._setup()

        self.maskFFT()

    def _setup(self):
        self._Gpx = (self._Px - self.s[1] / 2)
        self._Gpy = (self._Py - self.s[0] / 2)
        self._Gx = self._Gpx / self.s[1]
        self._Gy = self._Gpy / self.s[0]

        self.makeGaussMask(self._sigma)

    def makeGaussMask(self, sigma):
        xx, yy = np.meshgrid(np.arange(self.s[1]), np.arange(self.s[0]))
        xx = xx - np.floor(self.s[1] / 2)
        yy = yy - np.floor(self.s[0] / 2)

        self._mask = np.exp(-1 * ((xx - self._Px) ** 2 + (yy - self._Py) ** 2)
                            / (2 * sigma ** 2))

        # fftshift shift to make applying to mask easier
        self._mask = np.fft.fftshift(self._mask)

    def maskFFT(self):
        self._Hg = np.multiply(self._Hg, self._mask)

    @property
    def braggImage(self):
        # to return (2x) the real part of the IFFT of the masked FFT
        return np.multiply(2, np.fft.ifft2(self._Hg).real)

    @property
    def maskImage(self):
        return np.fft.fftshift(self._mask)

    @property
    def hgImage(self):
        return np.fft.fftshift(np.abs(np.log(self._Hg + 1)))

    @property
    def rawPhase(self):
        # to return the phase of the IFFT of the masked FFT
        return np.angle(np.fft.ifft2(self._Hg))

    @property
    def phase(self):
        # to return the phase - 2*Pi*(g.r)
        xx, yy = np.meshgrid(np.arange(self.s[1]), np.arange(self.s[0]))
        return self.rawPhase - 2 * np.pi * (xx * self._Gx + yy * self._Gy)

    @property
    def normPhase(self):
        # returns the phase clamped between -pi and pi
        # keep a copy of this as it will need to be displayed
        # and used in calculation
        try:
            return self._normPhase
        except AttributeError:
            self._calcNormPhase()
            return self._normPhase

    def _calcNormPhase(self):
        tempPhase = self.phase
        self._normPhase = tempPhase - np.round(tempPhase /
                                               (2 * np.pi)) * 2 * np.pi

    @property
    def expDifferential(self):  # I think axis 0 is y?
        # get the differential of the phase
        # Can't use numpy.diff as it truncates the returned array
        expPhase = np.exp(1j * self.normPhase)

        xkernel = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]]) / 6
        ykernel = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]]) / 6

        # use multithreading here? yay!
        temp = convolve2d(expPhase, xkernel, mode='same')
        ddx = np.imag(np.conj(expPhase) * temp)

        temp = convolve2d(expPhase, ykernel, mode='same')
        ddy = np.imag(np.conj(expPhase) * temp)

        return ddx, -ddy

    def refinePhase(self, xmin, xmax, ymin, ymax):

        region = self.normPhase[ymin:(ymax + 1), xmin:(xmax + 1)]
        s = region.shape
        l = region.size
        xx, yy = np.meshgrid(np.arange(s[1]), np.arange(s[0]))

        y = np.resize(region.T, (l, 1))

        X = np.concatenate((np.ones(y.shape),
                            np.resize(xx.T, (l, 1)),
                            np.resize(yy.T, (l, 1))),
                           1)

        coef = np.linalg.lstsq(X, y)

        b = coef[0][1][0]
        c = coef[0][2][0]

        dPx = b / (2 * np.pi) * self.s[1]
        dPy = c / (2 * np.pi) * self.s[0]

        self._Px = self._Px + dPx
        self._Py = self._Py + dPy

        self._setup()
        self._calcNormPhase()
