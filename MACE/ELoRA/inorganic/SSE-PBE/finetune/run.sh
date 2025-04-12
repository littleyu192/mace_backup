#!/bin/bash

#DSUB -n mace-MPtrj
#DSUB -A root.l6eub2ic
#DSUB -q root.default
#DSUB -R cpu=32;gpu=1;mem=1024
#DSUB -N 1
#DSUB -oo mace-MPtrj_%J_out.log
#DSUB -eo mace-MPtrj_%J_err.log

source ~/envs/env_mace.sh

python ~/opt/mace/scripts/run_train.py \
    --name="SSE-PBE" \
    --train_file="./dataset/train.xyz" \
    --valid_file="./dataset/valid.xyz" \
    --E0s="average" \
    --foundation_model="/home/l6eub2ic/whcs-share31/wangchen/mace/MPtrj/2024-01-07-mace-128-L2_epoch-199.model" \
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
    --batch_size=2 \
    --valid_batch_size=2 \
    --lr_factor=0.8 \
    --scheduler_patience=5 \
    --ema \
    --ema_decay=0.995 \
    --max_num_epochs=200 \
    --error_table="TotalRMSE" \
    --device=cuda \
    --seed=123 \
    --clip_grad=100 \
    --save_cpu \