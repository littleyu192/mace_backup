#!/bin/sh
#SBATCH --partition=a100
#SBATCH --job-name=MACE-L0
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --cpus-per-task=16
#SBATCH --gres=gpu:4

DISTRIBUTED_ARGS="
    --nproc_per_node=4
"

torchrun $DISTRIBUTED_ARGS /share/home/husiyu/software/MACE/mace/mace/cli/run_train.py \
    --name="L0" \
    --train_file="/share/home/husiyu/software/MACE/data/MPtri-datasets/postprocess_data/train" \
    --valid_file="/share/home/husiyu/software/MACE/data/MPtri-datasets/postprocess_data/val" \
    --statistics_file="/share/home/husiyu/software/MACE/data/MPtri-datasets/postprocess_data/statistics.json" \
    --loss='universal' \
    --energy_weight=1 \
    --forces_weight=10 \
    --compute_stress=True \
    --stress_weight=100 \
    --stress_key='stress' \
    --eval_interval=1 \
    --error_table='PerAtomMAE' \
    --model="ScaleShiftMACE" \
    --interaction_first="RealAgnosticResidualInteractionBlock" \
    --interaction="RealAgnosticResidualInteractionBlock" \
    --num_interactions=2 \
    --correlation=3 \
    --max_ell=3 \
    --r_max=6.0 \
    --max_L=0 \
    --num_channels=128 \
    --num_radial_basis=10 \
    --MLP_irreps="16x0e" \
    --scaling='rms_forces_scaling' \
    --num_workers=16 \
    --lr=0.005 \
    --weight_decay=1e-8 \
    --ema \
    --ema_decay=0.995 \
    --scheduler_patience=5 \
    --batch_size=16 \
    --valid_batch_size=32 \
    --max_num_epochs=200 \
    --patience=50 \
    --amsgrad \
    --device=cuda \
    --distributed \
    --seed=1 \
    --clip_grad=100 \
    --keep_checkpoints \
    --save_cpu

# train by KF
# torchrun $DISTRIBUTED_ARGS /share/home/husiyu/software/MACE/mace/mace/cli/run_train.py \
#     --name="L0" \
#     --train_file="/share/home/husiyu/software/MACE/data/MPtri-datasets/postprocess_data/train" \
#     --valid_file="/share/home/husiyu/software/MACE/data/MPtri-datasets/postprocess_data/val" \
#     --statistics_file="/share/home/husiyu/software/MACE/data/MPtri-datasets/postprocess_data/statistics.json" \
#     --loss='universal' \
#     --energy_weight=1 \
#     --forces_weight=10 \
#     --compute_stress=True \
#     --stress_weight=100 \
#     --stress_key='stress' \
#     --eval_interval=1 \
#     --error_table='PerAtomMAE' \
#     --model="ScaleShiftMACE" \
#     --interaction_first="RealAgnosticResidualInteractionBlock" \
#     --interaction="RealAgnosticResidualInteractionBlock" \
#     --num_interactions=2 \
#     --correlation=3 \
#     --max_ell=3 \
#     --r_max=6.0 \
#     --max_L=0 \
#     --num_channels=128 \
#     --num_radial_basis=10 \
#     --MLP_irreps="16x0e" \
#     --scaling='rms_forces_scaling' \
#     --num_workers=16 \
#     --lr=0.005 \
#     --weight_decay=1e-8 \
#     --ema \
#     --ema_decay=0.995 \
#     --scheduler_patience=5 \
#     --batch_size=16 \
#     --valid_batch_size=32 \
#     --max_num_epochs=200 \
#     --patience=50 \
#     --amsgrad \
#     --device=cuda \
#     --distributed \
#     --seed=1 \
#     --clip_grad=100 \
#     --keep_checkpoints \
#     --optimizer=LKF \
#     --save_cpu
