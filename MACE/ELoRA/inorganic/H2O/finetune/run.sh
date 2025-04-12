#!/bin/bash

#SBATCH --partition=a100
#SBATCH --job-name=mace
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --gres=gpu:1

python ~/opt/mace/scripts/run_train.py \
    --name="H2O" \
    --train_file="./dataset/train.xyz" \
    --valid_file="./dataset/valid.xyz" \
    --E0s="average" \
    --foundation_model="/share/home/wangchen/work/mace/MPtrj/2024-01-07-mace-128-L2_epoch-199.model" \
    --model="ScaleShiftMACE" \
    --interaction_first="RealAgnosticResidualInteractionBlock" \
    --interaction="RealAgnosticResidualInteractionBlock" \
    --num_interactions=2 \
    --correlation=3 \
    --max_ell=3 \
    --r_max=6.0 \
    --max_L=2 \
    --num_channels=128 \
    --num_radial_basis=10 \
    --MLP_irreps="16x0e" \
    --scaling='rms_forces_scaling' \
    --loss="ef" \
    --energy_weight=1 \
    --forces_weight=1000 \
    --amsgrad \
    --lr=0.005 \
    --weight_decay=1e-8 \
    --batch_size=1 \
    --valid_batch_size=1 \
    --lr_factor=0.8 \
    --scheduler_patience=5 \
    --ema \
    --ema_decay=0.995 \
    --max_num_epochs=10 \
    --error_table="TotalRMSE" \
    --device=cuda \
    --seed=123 \
    --clip_grad=100 \
    --save_cpu \
    --eval_interval=1 \
    --restart_latest \