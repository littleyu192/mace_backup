#!/bin/bash
#SBATCH --partition=3090
#SBATCH --job-name=Test
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --gres=shard:1


module load conda/3-2020.07 cudnn/12 gcc/11.4.0 
source activate pace

cd /share/home/zhujie/zhujie/project/PACE

/share/home/zhujie/.conda/envs/pace/bin/python main_rmd17_for_example.py --device 0 --task aspirin --output_dir ./results/pace/aspirin --num_bessel 6

