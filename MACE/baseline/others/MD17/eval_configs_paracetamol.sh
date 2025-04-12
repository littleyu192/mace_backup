#!/bin/bash

#SBATCH --partition=GPU-8A100
#SBATCH --job-name=mace-paracetamol
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --qos=gpu_8a100

source ~/work/mace/env.sh

python ~/work/mace/mace/scripts/eval_configs.py \
    --configs="./dataset/paracetamol_test.xyz" \
    --model="paracetamol.model" \
    --output="./tests/paracetamol_test.xyz" \
    --device=cuda \
    --batch_size=5 \