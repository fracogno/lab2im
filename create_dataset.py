import os
from lab2im import utils
from lab2im.image_generator import ImageGenerator
import glob
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--result_dir", type=str, required=True)
parser.add_argument("--filename", type=str, required=True)
args = parser.parse_args()

# path where to save the generated image
result_dir = args.result_dir

# Parameters
AUGMENTATIONS_PER_PATIENT = 50

filename = args.filename
patient_name = filename.split("/")[-1]

for i in range(AUGMENTATIONS_PER_PATIENT):
    brain_generator = ImageGenerator(labels_dir=filename + "/mri/map_seg.nii",
                                     blur_background=False)
    im, lab = brain_generator.generate_image()
    
    # Mask background
    im[lab==0] = 0.

    # Subtract mean without background
    im[im!=0] -= im[im!=0].mean()

    # Divide by STD, the smaller what inside the uniform, the broader the distribution is
    im = im / float(round(np.random.uniform(10., 60.), 4) * im.std())
    im = np.float32(im)

    utils.save_volume(im, brain_generator.aff, brain_generator.header, result_dir + patient_name + "_" + str(i) + '_brain.nii.gz')
    utils.save_volume(np.int32(lab), brain_generator.aff, brain_generator.header, result_dir + patient_name + "_" + str(i) + '_seg.nii.gz')
    
    del im
    del lab
    del brain_generator
