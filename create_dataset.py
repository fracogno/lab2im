import os
from lab2im import utils
from lab2im.image_generator import ImageGenerator
import glob
import numpy as np


# path where to save the generated image
result_dir = '/scratch/cai/francesco/lab2im/dataset_QSM/'

# Parameters
AUGMENTATIONS_PER_PATIENT = 100

for mode in ["train", "val"]:

	# Find filenames
	folders = glob.glob("/scratch/cai/francesco/lab2im/original_data/" + mode + "/*")
	folders.sort()

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

	        # Divide by STD, the smaller what inside the uniform, the broader the distribution is
	        im = im / float(round(np.random.uniform(10., 60.), 4) * im.std())
	        im = np.float32(im)

	        utils.save_volume(im, brain_generator.aff, brain_generator.header, result_dir + mode + "/" + patient_name + "_" + str(i) + '_brain.nii.gz')
	        utils.save_volume(lab, brain_generator.aff, brain_generator.header, result_dir + mode + "/" + patient_name + "_" + str(i) + '_seg.nii.gz')
	        
	        del im
	        del lab
	        del brain_generator
