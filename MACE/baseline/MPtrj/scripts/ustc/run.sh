#!/bin/bash

#SBATCH --partition=GPU-8A100
#SBATCH --job-name=mace-MPtrj
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=64
#SBATCH --gres=gpu:8
#SBATCH --qos=gpu_8a100

srun ./L0.sh