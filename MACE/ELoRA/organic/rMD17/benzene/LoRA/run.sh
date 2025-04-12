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
    --name="benzene" \
    --train_file="./dataset/train.xyz" \
    --valid_file="./dataset/valid.xyz" \
    --E0s='average' \
    --foundation_model="/home/l6eub2ic/whcs-share31/wangchen/mace/MPtrj/MACE-OFF23_medium.model" \
    --model="MACE" \
    --loss="ef" \
    --num_interactions=2 \
    --num_channels=128 \
    --max_L=1 \
    --correlation=3 \
    --r_max=5.0 \
    --lr=0.005 \
    --forces_weight=1000 \
    --energy_weight=1 \
    --weight_decay=1e-8 \
    --clip_grad=100 \
    --batch_size=5 \
    --valid_batch_size=5 \
    --max_num_epochs=500 \
    --scheduler_patience=5 \
    --ema \
    --ema_decay=0.995 \
    --error_table="TotalRMSE" \
    --default_dtype="float64"\
    --device=cuda \
    --seed=123 \
    --save_cpu \