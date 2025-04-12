#!/bin/bash

#SBATCH --partition=GPU-8A100
#SBATCH --job-name=mace-AcAc
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --qos=gpu_8a100

source ~/work/mace/env.sh

python ~/work/mace/mace/scripts/eval_configs.py \
    --configs="./dataset/test_MD_300K.xyz" \
    --model="AcAc.model" \
    --output="./tests/test_MD_300K.xyz" \
    --device=cuda \
    --batch_size=5 \
& wait

python ~/work/mace/mace/scripts/eval_configs.py \
    --configs="./dataset/test_MD_600K.xyz" \
    --model="AcAc.model" \
    --output="./tests/test_MD_600K.xyz" \
    --device=cuda \
    --batch_size=5 \
& wait