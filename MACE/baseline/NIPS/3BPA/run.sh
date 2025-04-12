#!/bin/bash

#SBATCH --partition=GPU-8A100
#SBATCH --job-name=mace-3BPA
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --qos=gpu_8a100

source ~/work/mace/env.sh

python ~/work/mace/mace/scripts/run_train.py \
    --name="3BPA-L2" \
    --train_file="./dataset/train_300K.xyz" \
    --valid_fraction=0.1 \
    --test_file="./dataset/test_300K.xyz" \
    --E0s='{1:-13.587222780835477, 6:-1029.4889999855063, 7:-1484.9814568572233, 8:-2041.9816003861047}' \
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
    --max_num_epochs=1500 \
    --error_table="TotalRMSE" \
    --device=cuda \
    --seed=123 \