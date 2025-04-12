#!/bin/bash

#SBATCH --partition=a100
#SBATCH --job-name=mace
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --gres=gpu:1

python ~/opt/mace/scripts/run_train.py \
    --name="3BPA" \
    --train_file="./dataset/train_300K.xyz" \
    --valid_fraction=0.1 \
    --test_file="./dataset/test_300K.xyz" \
    --E0s='average' \
    --foundation_model="/share/home/wangchen/work/mace/MPtrj/MACE-OFF23_medium.model" \
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