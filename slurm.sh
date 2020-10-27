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

srun -n 1 python3 create_dataset.py
conda deactivate
