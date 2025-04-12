#!/bin/bash

#SBATCH --partition=GPU-8A100
#SBATCH --job-name=mace-aspirin
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --qos=gpu_8a100

source ~/work/mace/env.sh

python ~/work/mace/mace/scripts/run_train.py \
    --name="aspirin" \
    --train_file="./dataset/aspirin_train.xyz" \
    --valid_fraction=0.05 \
    --test_file="./dataset/aspirin_test.xyz" \
    --E0s='average' \
    --model="ScaleShiftMACE" \
    --num_channels=256 \
    --max_ell=3 \
    --max_L=2 \
    --num_radial_basis=8 \
    --num_cutoff_basis=5 \
    --gate="silu" \
    --MLP_irreps="16x0e" \
    --r_max=5.0 \
    --loss="ef" \
    --energy_weight=1 \
    --forces_weight=1000 \
    --amsgrad \
    --lr=0.01 \
    --batch_size=5 \
    --valid_batch_size=5 \
    --lr_factor=0.8 \
    --scheduler_patience=50 \
    --ema \
    --ema_decay=0.99 \
    --max_num_epochs=2000 \
    --error_table="TotalRMSE" \
    --device=cuda \
    --seed=123 \