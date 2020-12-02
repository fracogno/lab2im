#!/bin/bash
#SBATCH -N 1
#SBATCH --job-name=lab2im
#SBATCH -n 1
#SBATCH -c 6
#SBATCH --mem=50000
#SBATCH -o out_wiener.txt
#SBATCH -e error_wiener.txt
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1

module load anaconda/3.6
#conda create -y --name lab2im_env python=3.6
conda env list

#conda install -y -q --name lab2im_env -c conda-forge --file requirements.txt
source activate lab2im_env

dataset_foldername="extracted"

base_path=$(pwd)"/dataset/"
dataset_path=$base_path$dataset_foldername
result_path=$dataset_path"_augmented"

mkdir $result_path
for mode in "train" "val"
do		
	mkdir $result_path"/"$mode"/"

	mode_path=$dataset_path"/"$mode"/"
	for file in $(ls $mode_path)
	do
		srun -n 1 python3 create_dataset.py --result_dir $result_path"/"$mode"/" --filename $mode_path$file
	done
done

conda deactivate
