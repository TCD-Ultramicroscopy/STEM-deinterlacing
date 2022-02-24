import numpy as np
import pickle


# this class just holds the variables (and calculates the field) just so this information can be stored and applied to
# all the images the same
class WaveGen:
    def __init__(self, freq, amp, phase, angle):
        self.freq = freq
        self.amp = amp
        self.phase = phase
        self.angle = angle

    def gen(self, time):
        distortion_amp = self.amp * np.sin(self.freq * (10 ** -6) * time * 2 * np.pi + self.phase)

        distortion_x = distortion_amp * np.cos(self.angle)
        distortion_y = distortion_amp * np.sin(self.angle)

        return distortion_y, distortion_x


#
# Load waves from file if desired, else generates from scratch
#
def get_distortions(n_freq=None, freq_range=None, amp_range=None, reuse=False, save=True):
    if reuse:
        with open("waves.pickle", "rb") as fp:  # Unpickling
            wave_info = pickle.load(fp)
            return wave_info

    waves = generate_distortions(n_freq, freq_range, amp_range)
    output = {'waves': waves, 'n_freq': n_freq, 'freq_range': freq_range, 'amp_range': amp_range}

    if save:
        with open("waves.pickle", "wb") as fp:  # Pickling
            pickle.dump(output, fp)

    return output


def normalise_amp(amp, freq_range, freq):
    return 0.3 * amp * freq_range[1] / freq


def generate_distortions(n_freq, freq_range, amp_range):
    waves = []

    for i in range(n_freq):
        # pick our frequency, phase, amplitude and direction
        freq = np.random.uniform(freq_range[0], freq_range[1])
        phase = np.random.uniform(0, 2 * np.pi)
        amp = np.random.uniform(amp_range[0], amp_range[1])
        angle = np.random.uniform(0, 2 * np.pi)  # the direction the wave travels across the image

        amp = normalise_amp(amp, freq_range, freq)

        waves.append(WaveGen(freq, amp, phase, angle))

    return waves