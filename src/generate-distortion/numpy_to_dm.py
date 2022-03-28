import numpy as np
import DigitalMicrograph as DM
import os

base_dir = r''

for bf in os.listdir(base_dir):
    top_dir = os.path.join(base_dir, bf)
    if not os.path.isdir(top_dir) or not bf.startswith('output_'):
        continue

    for sub_dir in ['full', 'full_rot', 'int', 'int_rot']:
        sd = os.path.join(top_dir, sub_dir)
        
        for f in os.listdir(sd):
            f_path = os.path.join(sd, f)
            f_name, f_ext = os.path.splitext(f)
                        
            print(f_name + f_ext)
            
            if f_ext == '.npy':
                img = None
                out_path = os.path.join(sd, f_name)
                if not os.path.exists(out_path + '.dm3') and not os.path.exists(out_path + '.dm4'):
                    
                    print('saving as DM')
                    
                    im_data = np.load(f_path)
                    
                    img = DM.CreateImage(im_data)
                    
                    # # img.ShowImage()
                    
                    img.SaveAsGatan(out_path)
                else:
                    print('output already exists')
                
                out_path_001 = os.path.join(sd, 'Average Through Stack Non-rigid Aligned ' + f_name) + '.dm4'
                if 'nf_001' in f_name and not os.path.exists(out_path_001):
                    print('saving single stack fake aligned image')
                    if img is None:
                        im_data = np.load(f_path)
                        img = DM.CreateImage(im_data)
                    img.SaveAsGatan(out_path_001)
                
                print('boop')
                
                del img
            else:
                print('not npy file to convert')

print("Full boop")