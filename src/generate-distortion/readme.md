# Generate distortion

This folder contains scripts for generating distortion for simulated images

## Usage

The scripts are split into multiple parts. In general the script run order should be:

- generate-perfect/generate_perfect.py - This creates the input image. Alternatively the output of a proper simulation can be used.
- create_datasets.py - This generates the distortion and applies it to the perfect image for both interlaced and non-interlaced (also scan rotation and non-rotation)
- numpy_to_dm.py - This runs in DigitalMicrograph to convert the .npy files to .dm4 files (needed for Smart Align)
- organise_for_smart_align.py - Puts all the files in one folder so batch Smart Align can be used
- Run Smart Align using 'repeat alignment of same signal' (you need to do one manually with the correct settings)
- organise_after_smar_align.py - Returns aligned data to correct folders.

After this, the strain analysis can be performed using scripts in the 'process-strain' folder.