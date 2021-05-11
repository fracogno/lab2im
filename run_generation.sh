
# How many samples per segmentation map
AUGMENTATIONS=30

# Where segmentation maps are saved
dataset_path=$(pwd)"/dataset/extracted"

# Where to save them
result_path=$dataset_path"_augmented_"$AUGMENTATIONS
mkdir $result_path

# Create training and validation
for mode in "train" "val"
do		
	mkdir $result_path"/"$mode"/"

	mode_path=$dataset_path"/"$mode"/"
	for file in $(ls $mode_path)
	do
		python3 create_dataset.py --result_dir $result_path"/"$mode"/" --filename $mode_path$file --augmentations $AUGMENTATIONS
	done
done