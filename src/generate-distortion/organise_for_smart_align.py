###############################################################################
#
# organise_for_smart_align.py
#
# Created by Jonathan J. P. Peters
#
# This takes the data from the organised folders and puts it into two folders
# (one with scan rotations and one without). This lets you use the batch
# processing on smart align to do everything at once.
#
###############################################################################

import sys
import os
import shutil
from base_dir import base_dir

working_folder = 'smart_align_working'
working_dir = os.path.join(base_dir, working_folder)

redo_copy = False

if os.path.exists(working_dir) and redo_copy:
    shutil.rmtree(working_dir)

if not os.path.exists(working_dir):
    os.mkdir(working_dir)

for bf in os.listdir(base_dir):
    top_dir = os.path.join(base_dir, bf)
    if not os.path.isdir(top_dir) or not bf.startswith('output_'):
        continue

    use_list = []
    for i in range(21):
        use_list.append(f'output_{i}')
    if bf not in use_list:
        continue

    for sub_dir in ['full', 'full_rot', 'int', 'int_rot']:
        sd = os.path.join(top_dir, sub_dir)

        for f in os.listdir(sd):
            f_path = os.path.join(sd, f)
            f_name, f_ext = os.path.splitext(f)

            print(os.path.join(sd, f_name + f_ext))

            if f_ext in ['.dm4', '.dm3'] and f_name.startswith('image_nf_'):
                print('file to analyse')

                averaged_path = os.path.join(sd, 'Average Through Stack Non-rigid Aligned ' + f_name) + '.dm4'

                if os.path.exists(averaged_path):
                    print('no need to do alignment')
                    continue

                out_fname = bf.strip('output_') + '--' + sub_dir + '--' + f_name + f_ext
                if sub_dir in ['full_rot', 'int_rot']:
                    out_sf = 'rot'
                else:
                    out_sf = 'full'

                if not os.path.exists(os.path.join(working_dir, out_sf)):
                    os.mkdir(os.path.join(working_dir, out_sf))

                src_pth = f_path
                dst_pth = os.path.join(*[working_dir, out_sf, out_fname])

                if os.path.exists(dst_pth):
                    if os.path.getsize(dst_pth) != os.path.getsize(src_pth):
                        print(f'possible issue with file sizes: {src_pth}')

                    print('file already exists')
                    continue

                shutil.copy(src_pth, dst_pth)