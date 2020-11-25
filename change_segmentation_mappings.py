import glob
import nibabel as nib
import numpy as np
import pickle
import copy

# Class mappings
mappings = {
	0  : 0, 	# Background
	2  : 1, 	# Cerebral-White-Matter
	3  : 2, 	# Cerebral-Cortex
	4  : 12, 	# Merged with 24 to CSF
	5  : 12,	# Merged with 24 to CSF
	7  : 3,		# Cerebellum-White-Matter
	8  : 4,  	# Cerebellum-Cortex
	10 : 5, 	# Thalamus-Proper
	11 : 6, 	# Caudate
	12 : 7,		# Putamen
	13 : 8, 	# Pallidum
	14 : 12,  	# Merged with 24 to CSF
	15 : 12,  	# Merged with 24 to CSF
	16 : 9, 	# Brain-Stem
	17 : 10, 	# Hippocampus
	18 : 11, 	# Amygdala
	24 : 12,	# CSF
	26 : 13, 	# Accumbens-area
	28 : 14,	# VentralDC
	30 : 7,		# Merged with 12 Putamen
	31 : 12,	# Merged with 24 to CSF
	41 : 1,		# Merged with 2 to Cerebral-White-Matter
	42 : 2,		# Merged with 3 to Cerebral-Cortex
	43 : 12,	# Merged with 24 to CSF
	44 : 12,	# Merged with 24 to CSF
	46 : 3,		# Merged with 7 to Cerebellum-White-Matter
	47 : 4,		# Merged with 8 to Cerebellum-Cortex
	49 : 5,		# Merged with 10 to Thalamus-Proper
	50 : 6,		# Merged with 11 to Caudate
	51 : 7, 	# Merged with 12 to Putamen
	52 : 8, 	# Merged with 13 to Pallidum
	53 : 10, 	# Merged with 17 to Hippocampus
	54 : 11,	# Merged with 18 to Amygdala
	58 : 13,	# Merged with 26 to Accumbens-area
	60 : 14,	# Merged with 28 to VentralDC
	62 : 7,		# Merged with 12 Putamen
	63 : 12,	# Merged with 24 to CSF
	72 : 12,	# Merged with 24 to CSF
	77 : 1,		# Merged with 2 to Cerebral-White-Matter
	80 : 2,		# Merged with 3 to Cerebral-Cortex
	85 : 1,		# Merged with 2 to Cerebral-White-Matter
	251 : 15,	# Corpus Callosum
	252 : 15,	# Merged with 251 to Corpus Callosum
	253 : 15,	# Merged with 251 to Corpus Callosum
	254 : 15,	# Merged with 251 to Corpus Callosum
	255 : 15	# Merged with 251 to Corpus Callosum
}


base_path = "/mnt/ResearchFS/francesco/data/"
classes = set()
filenames = glob.glob(base_path + "freesurferResults/*")
filenames.sort()
for filename in filenames:
	data = nib.load(filename + "/mri/aseg.nii")
	volume = np.vectorize(mappings.get)(np.int32(data.get_fdata()))	
	classes.update(np.unique(volume))

	nib.save(nib.Nifti1Image(volume, data.affine, data.header), filename + "/mri/map_seg.nii")

	del data
	del volume

classes = list(classes)
classes.sort()
print(classes)
pickle.dump(classes, open( "classes.pkl", "wb"))
