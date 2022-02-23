import numpy as np
import DigitalMicrograph as DM
import os

# Set this to the folder with the .npy files
dir = r''

for f in os.listdir(dir):
    f_path = os.path.join(dir, f)
    f_name, f_ext = os.path.splitext(f_path)
    
    print(f_name)
    
    if f_ext == '.npy':
    
        im_data = np.load(f_path)
        
        img = DM.CreateImage(im_data)

        # img.ShowImage()
        
        img.SaveAsGatan(f_name)