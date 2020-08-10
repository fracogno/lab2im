# Very simple script showing how to generate new images with random contrast

import os
from lab2im import utils
from lab2im.image_generator import ImageGenerator


# path of the input label map
path_label_map = './data_example/brain_label_map.nii.gz'
# path where to save the generated image
resulr_dir = './generated_images'

# save output image and label map
if not os.path.exists(os.path.join(resulr_dir)):
    os.mkdir(resulr_dir)

# generate an image from the label map.
# Because the image is spatially deformed, we also output the corresponding deformed label map.
brain_generator = ImageGenerator(path_label_map)
for i in range(10):
    im, lab = brain_generator.generate_image()

    utils.save_volume(im, brain_generator.aff, brain_generator.header, os.path.join(resulr_dir, 'brain-'+str(i)+'.nii.gz'))
    utils.save_volume(lab, brain_generator.aff, brain_generator.header, os.path.join(resulr_dir, 'labels-'+str(i)+'.nii.gz'))
