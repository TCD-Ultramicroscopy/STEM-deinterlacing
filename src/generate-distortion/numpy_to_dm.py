import numpy as np
import DigitalMicrograph as DM
import os

# Set this to the folder with the .npy files
top_dir = r''

for sub_dir in ['full', 'full_rot', 'int', 'int_rot']:

    sd = os.poath.join(top_dir, sub_dir)

    for f in os.listdir(sd):
        f_path = os.path.join(sd, f)
        f_name, f_ext = os.path.splitext(f_path)
        
        print(f_name)
        
        if f_ext == '.npy':
        
            im_data = np.load(f_path)
            
            img = DM.CreateImage(im_data)

            # img.ShowImage()
            
            img.SaveAsGatan(f_name)