import os
import sys
from read_dm3 import DM3
import numpy as np
import re
import matplotlib.pyplot as plt
from scipy.stats import sem
import tifffile as tf

import pyGPA as gpa

base_path = r''

sub_folders = ['full', 'full_rot', 'int', 'int_rot']

out_data = {}

for sf in sub_folders:
    data_dir = os.path.join(base_path, sf)

    for file in os.listdir(data_dir):

        re_string = r'Average Through Stack Non-rigid Aligned image_nf_(\d+)_dt_([\d-]+)\.dm4'

        re_expr = re.compile(re_string)

        re_match = re_expr.match(file)

        if re_match is None:
            continue
        
        frames_str = re_match.groups()[0]
        dwell_str = re_match.groups()[1].replace('-', '.')

        frames = int(frames_str)
        dwell = float(dwell_str)

        # these are the paramters for the strain measurement
        sigma = 4.166
        x1 = 29
        y1 = -22
        x2 = 22
        y2 = 29

        input_file_path = os.path.join(data_dir, file)

        image = DM3(input_file_path).image.astype(np.float64)

        # Hann window
        image *= np.hanning(image.shape[1])
        image *= np.hanning(image.shape[0])[:, np.newaxis]

        s = gpa.GPA(image)

        s.getPhase(0, x1, y1, sigma)
        s.getPhase(1, x2, y2, sigma)

        s.getStrains()

        crop = 70

        print(input_file_path)
        print(frames)
        print(dwell)
        # # plt.imshow(s.Eyy)
        # # plt.imshow(np.log(np.abs(s.Phase[0]._Hg) + 1))
        # plt.imshow(s.Eyy[crop:-crop, crop:-crop])
        # plt.show()

        # tf.imsave(os.path.join(data_dir, 'EYY ' + os.path.splitext(file)[0] + '.tif'), s.Eyy.astype(np.float32))

        
        eyy_sig = np.std(s.Eyy[crop:-crop, crop:-crop])
        #eyy_sig = np.std(s.Eyy[crop:-crop, 20:-20])

        if sf not in out_data.keys():
            out_data[sf] = {'frames': [frames], 'variation': [eyy_sig]}
        else:
            out_data[sf]['frames'].append(frames)
            out_data[sf]['variation'].append(eyy_sig)



for k in out_data.keys():

    x = np.array(out_data[k]['frames'])
    y = np.array(out_data[k]['variation'])

    print(k)

    if k in ['int', 'int_rot']:
        x = x / 2

    print(x)

    plt.plot(x, y, '-o', label=k)

plt.legend()

plt.xlabel("Dose (full frames)")
plt.ylabel("e$_{yy}$ standard deviation")
plt.show()