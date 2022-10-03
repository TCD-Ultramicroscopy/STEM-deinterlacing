# Generate distortion

This folder contains scripts for generating distortion for simulated images. It encompasses creation of the initial image (if you want to avoid a detailed simulation), application of a distortion field, and scripts to organise data to make it more convenient to work with SmartAlign.

## Usage

First the output folder location should be defined in ``base_dir.py``, this also needs to be defined in the ``numpy_to_dm.py`` file.

The scripts are split into multiple parts. In general the script run order should be:

1. ``generate-perfect/generate_perfect.py`` - This creates the input image. Alternatively the output of a proper simulation can be used.
2. ``create_datasets.py`` - This generates the distortion and applies it to the perfect image for both interlaced and non-interlaced (also scan rotation and non-rotation)
3. ``numpy_to_dm.py`` - This runs in DigitalMicrograph to convert the .npy files to .dm4 files (needed for Smart Align)
4. ``organise_for_smart_align.py`` - Puts all the files in one folder so batch Smart Align can be used
5. Run Smart Align using 'repeat alignment of same signal' (you need to do one manually with the correct settings)
6. ``organise_after_smar_align.py`` - Returns aligned data to correct folders.

After this, the strain analysis can be performed using scripts in the 'process-strain' folder.

There is a ``close_image_thread.s`` that was used in parallel with older versions of SmartAlign to close images as they were opened after reconstruction. This would fill memory and lead to issues. However, this has been fixed in later version of SmartAlign.