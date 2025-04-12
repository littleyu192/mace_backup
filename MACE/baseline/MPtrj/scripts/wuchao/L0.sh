#!/bin/bash

#DSUB -n mace-MPtrj
#DSUB -A root.l6eub2ic
#DSUB -q root.default
#DSUB -R cpu=128;gpu=4;mem=240000
#DSUB -N 4
#DSUB -oo mace-MPtrj_%J_out.log
#DSUB -eo mace-MPtrj_%J_err.log

NNODES=4
HOSTFILE=nodelist
touch $HOSTFILE
HOST=`hostname`
flock -x ${HOSTFILE} -c "echo ${HOST} >> ${HOSTFILE}"
MASTER_IP=`head -n 1 ${HOSTFILE}`
HOST_RANK=`sed -n "/${HOST}/=" ${HOSTFILE}`
let NODE_RANK=HOST_RANK-1

export NCCL_IB_HCA=mlx5_0:1,mlx5_1:1,mlx5_2:1,mlx5_3:1
export NCCL_IB_DISABLE=0
export NCCL_SOCKET_IFNAME=eth0
export NCCL_IB_GID_INDEX=3
#export NCCL_IB_TIMEOUT=23
export NCCL_IB_RETRY_CNT=7
#export NCCL_DEBUG=INFO
export NCCL_ASYNC_ERROR_HANDLING=1

DISTRIBUTED_ARGS="
    --nproc_per_node=4 \
    --nnodes=${NNODES} \
    --node_rank=${NODE_RANK} \
    --master_addr=${MASTER_IP} \
    --master_port=33647
"

source ~/envs/env_mace.sh

torchrun $DISTRIBUTED_ARGS ~/MLFF/MACE/mace/scripts/run_train.py \
    --name="L0" \
    --train_file="./dataset/processed_data/train" \
    --valid_file="./dataset/processed_data/val" \
    --statistics_file="./dataset/processed_data/statistics.json" \
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
    --num_workers=32 \
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
    --save_cpu \

if [ -f "${HOSTFILE}" ];then
    rm -rf ${HOSTFILE}
fi