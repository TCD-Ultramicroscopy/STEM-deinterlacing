import os
import sys
from read_dm3 import DM3
import numpy as np
import re
import matplotlib.pyplot as plt
from scipy.stats import sem
import tifffile as tf
from scipy.stats import sem as sci_sem
import pickle
from lmfit import Model, Parameters

import pyGPA as gpa

bp = r''
base_paths = []
for i in range (21):
    base_paths.append(os.path.join(bp, f'output_{i}'))

n_id = len(base_paths)

out_data = {}

reuse = True

out_pth = os.path.join(bp, "output_strain.pickle")
if reuse and os.path.exists(out_pth):

    with open(out_pth, "rb") as fp:  # Unpickling
        out_data =  pickle.load(fp)

else:

    id = 0
    for base_path in base_paths:
        sub_folders = ['full', 'full_rot', 'int', 'int_rot']

        out_data[f'{id}'] = {}

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

                print(input_file_path + "\n")
                # # plt.imshow(s.Eyy)
                # # plt.imshow(np.log(np.abs(s.Phase[0]._Hg) + 1))
                # plt.imshow(s.Eyy[crop:-crop, crop:-crop])
                # plt.show()

                # tf.imsave(os.path.join(data_dir, 'EYY ' + os.path.splitext(file)[0] + '.tif'), s.Eyy.astype(np.float32))


                exx_sig = np.std(s.Exx[crop:-crop, crop:-crop])
                exy_sig = np.std(s.Exy[crop:-crop, crop:-crop])
                eyy_sig = np.std(s.Eyy[crop:-crop, crop:-crop])
                eyx_sig = np.std(s.Eyx[crop:-crop, crop:-crop])
                #eyy_sig = np.std(s.Eyy[crop:-crop, 20:-20])

                total_sig = exx_sig + exy_sig + eyy_sig + eyx_sig

                if sf not in out_data[f'{id}'].keys():
                    out_data[f'{id}'][sf] = {'frames': [frames],
                                             'total_sig': [total_sig],
                                             'exx_sig': [exx_sig],
                                             'exy_sig': [exy_sig],
                                             'eyy_sig': [eyy_sig],
                                             'eyx_sig': [eyx_sig]}
                else:
                    out_data[f'{id}'][sf]['frames'].append(frames)
                    out_data[f'{id}'][sf]['total_sig'].append(total_sig)
                    out_data[f'{id}'][sf]['exx_sig'].append(exx_sig)
                    out_data[f'{id}'][sf]['exy_sig'].append(exy_sig)
                    out_data[f'{id}'][sf]['eyy_sig'].append(eyy_sig)
                    out_data[f'{id}'][sf]['eyx_sig'].append(eyx_sig)

        id += 1

    with open(out_pth, "wb") as fp:  # Pickling
        pickle.dump(out_data, fp)


# id = 0
# for k in out_data[f'{id}'].keys():
#
#     x = np.array(out_data[f'{id}'][k]['frames'])
#     y = np.array(out_data[f'{id}'][k]['variation'])
#
#     if k in ['int', 'int_rot']:
#         x = x / 2
#
#     plt.plot(x, y, '-o', label=k)
#
# plt.legend()
#
# plt.xlabel("Dose (full frames)")
# plt.ylabel("e$_{yy}$ standard deviation")
# plt.show()


plot_var = 'total_sig'

for k in out_data[f'0'].keys():
    for id in range(n_id):

        x = np.array(out_data[f'{id}'][k]['frames'])
        y = np.array(out_data[f'{id}'][k][plot_var])

        col = np.array([0.0, 0.0, 0.0])
        if k == 'full':
            col = np.array([31, 119, 180], dtype=np.float64) / 255
        elif k == 'full_rot':
            col = np.array([255, 127, 14], dtype=np.float64) / 255
        elif k == 'int':
            col = np.array([44, 160, 44], dtype=np.float64) / 255
        elif k == 'int_rot':
            col = np.array([214, 39, 40], dtype=np.float64) / 255

        col *= 1 - id / (2*n_id)

        plt.plot(x, y, 'o', color=col, label=k + f'_{id}')
        plt.legend()

plt.xlabel("Dose (full frames)")
plt.ylabel(plot_var)
plt.show()

def line_fit(x, a, b):
    return a / np.sqrt(x) + b

x = None
y = None

fit_model = Model(line_fit)
fit_params = Parameters()
fit_params.add('a', value=1.0)
fit_params.add('b', value=-0.001, vary=False)

plot_cols = {'full': 'C0', 'int': 'C1', 'full_rot': 'C2', 'int_rot': 'C3'}

for k in out_data[f'0'].keys():
    for id in range(n_id):

        if y is None:
            x = np.array(out_data[f'{id}'][k]['frames'])
            y = np.array(out_data[f'{id}'][k][plot_var])[np.newaxis, ...]
        else:
            y = np.concatenate((y, np.array(out_data[f'{id}'][k][plot_var])[np.newaxis, ...]), axis=0)

    mean = np.mean(y, axis=0)
    err = sci_sem(y, axis=0)

    # fit this line
    result = fit_model.fit(mean, fit_params, x=x, method='nelder')

    print(k)
    print(result.fit_report())
    print('-\n-\n-')

    c = plot_cols[k]

    xx = np.linspace(x[0], x[-1], 100)
    plt.plot(xx, result.eval(x=xx), color=c)

    plt.errorbar(x, mean, yerr=err, marker='o', label=k, capsize=5, linestyle='', color=c)
    plt.legend()

plt.xlabel("Dose (full frames)")
# plt.yscale('log')
plt.ylabel(plot_var)
plt.show()