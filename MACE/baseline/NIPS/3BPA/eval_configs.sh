#!/bin/bash

#SBATCH --partition=GPU-8A100
#SBATCH --job-name=mace-3BPA
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --qos=gpu_8a100

source ~/work/mace/env.sh

python ~/work/mace/mace/scripts/eval_configs.py \
    --configs="./dataset/test_300K.xyz" \
    --model="3BPA-L2.model" \
    --output="./tests/L2_test_300K.xyz" \
    --device=cuda \
    --batch_size=5 \
& wait

python ~/work/mace/mace/scripts/eval_configs.py \
    --configs="./dataset/test_600K.xyz" \
    --model="3BPA-L2.model" \
    --output="./tests/L2_test_600K.xyz" \
    --device=cuda \
    --batch_size=5 \
& wait

python ~/work/mace/mace/scripts/eval_configs.py \
    --configs="./dataset/test_1200K.xyz" \
    --model="3BPA-L2.model" \
    --output="./tests/L2_test_1200K.xyz" \
    --device=cuda \
    --batch_size=5 \
& wait

python ~/work/mace/mace/scripts/eval_configs.py \
    --configs="./dataset/test_dih.xyz" \
    --model="3BPA-L2.model" \
    --output="./tests/L2_test_dih.xyz" \
    --device=cuda \
    --batch_size=5 \
& wait