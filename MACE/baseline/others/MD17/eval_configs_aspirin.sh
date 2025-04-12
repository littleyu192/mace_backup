#!/bin/bash

#SBATCH --partition=GPU-8A100
#SBATCH --job-name=mace-aspirin
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --qos=gpu_8a100

source ~/work/mace/env.sh

python ~/work/mace/mace/scripts/eval_configs.py \
    --configs="./dataset/aspirin_test.xyz" \
    --model="aspirin.model" \
    --output="./tests/aspirin_test.xyz" \
    --device=cuda \
    --batch_size=5 \