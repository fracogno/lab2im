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
	255 : 15,	# Merged with 251 to Corpus Callosum
	1000 : 2,
	1001 : 2,
	1002 : 2,
	1003 : 2,
	1005 : 2,
	1006 : 2,
	1007 : 2,
	1008 : 2,
	1009 : 2,
	1010 : 2,
	1011 : 2,
	1012 : 2,
	1013 : 2,
	1014 : 2,
	1015 : 2,
	1016 : 2,
	1017 : 2,
	1018 : 2,
	1019 : 2,
	1020 : 2,
	1021 : 2,
	1022 : 2,
	1023 : 2,
	1024 : 2,
	1025 : 2,
	1026 : 2,
	1027 : 2,
	1028 : 2,
	1029 : 2,
	1030 : 2,
	1031 : 2,
	1032 : 2,
	1033 : 2,
	1034 : 2,
	1035 : 2,
	2000 : 2,
	2001 : 2,
	2002 : 2,
	2003 : 2,
	2005 : 2,
	2006 : 2,
	2007 : 2,
	2008 : 2,
	2009 : 2,
	2010 : 2,
	2011 : 2,
	2012 : 2,
	2013 : 2,
	2014 : 2,
	2015 : 2,
	2016 : 2,
	2017 : 2,
	2018 : 2,
	2019 : 2,
	2020 : 2,
	2021 : 2,
	2022 : 2,
	2023 : 2,
	2024 : 2,
	2025 : 2,
	2026 : 2,
	2027 : 2,
	2028 : 2,
	2029 : 2,
	2030 : 2,
	2031 : 2,
	2032 : 2,
	2033 : 2,
	2034 : 2,
	2035 : 2,
	3001 : 1,
	3002 : 1,
	3003 : 1,
	3005 : 1,
	3006 : 1,
	3007 : 1,
	3008 : 1,
	3009 : 1,
	3010 : 1,
	3011 : 1,
	3012 : 1,
	3013 : 1,
	3014 : 1,
	3015 : 1,
	3016 : 1,
	3017 : 1,
	3018 : 1,
	3019 : 1,
	3020 : 1,
	3021 : 1,
	3022 : 1,
	3023 : 1,
	3024 : 1,
	3025 : 1,
	3026 : 1,
	3027 : 1,
	3028 : 1,
	3029 : 1,
	3030 : 1,
	3031 : 1,
	3032 : 1,
	3033 : 1,
	3034 : 1,
	3035 : 1,
	4001 : 1,
	4002 : 1,
	4003 : 1,
	4005 : 1,
	4006 : 1,
	4007 : 1,
	4008 : 1,
	4009 : 1,
	4010 : 1,
	4011 : 1,
	4012 : 1,
	4013 : 1,
	4014 : 1,
	4015 : 1,
	4016 : 1,
	4017 : 1,
	4018 : 1,
	4019 : 1,
	4020 : 1,
	4021 : 1,
	4022 : 1,
	4023 : 1,
	4024 : 1,
	4025 : 1,
	4026 : 1,
	4027 : 1,
	4028 : 1,
	4029 : 1,
	4030 : 1,
	4031 : 1,
	4032 : 1,
	4033 : 1,
	4034 : 1,
	4035 : 1,
	5001 : 1,
	5002 : 1
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
