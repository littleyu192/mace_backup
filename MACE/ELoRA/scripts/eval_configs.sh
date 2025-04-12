#!/bin/bash

#SBATCH --partition=a100
#SBATCH --job-name=mace
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --gres=gpu:1

python ~/opt/mace/scripts/eval_configs.py \
    --configs="./dataset/test.xyz" \
    --model="./LoRA/AgAu.model" \
    --output="./tests/test.xyz" \
    --device=cuda \
    --batch_size=5 \