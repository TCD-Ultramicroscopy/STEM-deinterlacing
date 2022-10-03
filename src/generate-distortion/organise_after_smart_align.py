###############################################################################
#
# organise_after_smart_align.py
#
# Created by Jonathan J. P. Peters
#
# This takes the folder with the smartalign output and organises the data back
# into individual folders
#
###############################################################################

import os
import shutil
import re
from base_dir import base_dir

working_folder = r'smart_align_working'
working_dir = os.path.join(base_dir, working_folder)

for swf in ['full', 'rot']:

    swd = os.path.join(working_dir, swf)

    if not os.path.exists(swd):
        continue

    for f in os.listdir(swd):
        f_path = os.path.join(swd, f)
        f_name, f_ext = os.path.splitext(f)

        re_pattern = "Average Through Stack Non-rigid Aligned (\d+)--([a-z_]+)--(image_nf_\d+_dt_[\d\-]+)"

        re_matches = re.findall(re_pattern, f_name)

        print(f_name)

        if len(re_matches) != 1 or len(re_matches[0]) != 3:
            print('Could not find correct matches to file regex')
            continue
        else:
            print(f'Found: {re_matches[0][0]}, {re_matches[0][1]}')

        run_id = re_matches[0][0]
        run_type = re_matches[0][1]
        run_file = re_matches[0][2]

        run_folder = 'output_' + run_id
        run_dir = os.path.join(*[base_dir, run_folder, run_type])

        dst_file = 'Average Through Stack Non-rigid Aligned ' + run_file + f_ext
        dst_pth = os.path.join(run_dir, dst_file)

        if os.path.exists(dst_pth):
            # print("File exists, NOT copying")
            # continue

            print("File exists, BUT STILL copying")
            # continue

        print("File does not exist, copying")

        src_pth = f_path
        shutil.copy(src_pth, dst_pth)

        print('')