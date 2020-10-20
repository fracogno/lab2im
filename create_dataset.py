import os
from lab2im import utils
from lab2im.image_generator import ImageGenerator
import glob
import numpy as np


AUGMENTATIONS_PER_PATIENT = 100

# Find filenames
folders = glob.glob("/mnt/ResearchFS/francesco/data/extracted/*")
folders.sort()

# path where to save the generated image
resulr_dir = './dataset_QSM'

for filename in folders:
    patient_name = filename.split("/")[-1]

    for i in range(AUGMENTATIONS_PER_PATIENT):
        brain_generator = ImageGenerator(labels_dir=filename + "/mri/wmparc.nii",
                                         blur_background=False)
        im, lab = brain_generator.generate_image()
        
        # Mask background
        im[lab==0] = 0.

        # Subtract mean without background
        im[im!=0] -= im[im!=0].mean()

        # Divide by STD
        im = im / float(round(np.random.uniform(16., 25.), 4) * im.std())
        im = np.float32(im)

        utils.save_volume(im, brain_generator.aff, brain_generator.header, os.path.join(resulr_dir, patient_name + "_" + str(i) + '_brain.nii.gz'))
        utils.save_volume(lab, brain_generator.aff, brain_generator.header, os.path.join(resulr_dir, patient_name + "_" + str(i) + '_seg.nii.gz'))
