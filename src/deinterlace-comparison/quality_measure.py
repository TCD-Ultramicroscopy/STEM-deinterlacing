import numpy as np
from skimage.metrics import structural_similarity

def image_similarity(image_reference, image_2, method='root_mean_square_error'):
    if method =='root_mean_square_error':
        return _root_mean_square_error(image_reference, image_2)
    elif method =='structural_similarity':
        return _structural_similarity(image_reference, image_2)
    else:
        print("Not a valid image similarity measurment")
        return 0.0


def _root_mean_square_error(_image_reference, _image_2):

    image_reference = _image_reference[1:-1, 2:-2]

    image_2 = _image_2[1:-1, 2:-2]

    image_ref_range = np.max(image_reference) - np.min(image_reference)
    mse = np.sum(np.power(image_reference-image_2, 2)) / image_reference.size
    return np.sqrt(mse) / image_ref_range

def _structural_similarity(image_reference, image_2):
    return structural_similarity(image_reference, image_2)