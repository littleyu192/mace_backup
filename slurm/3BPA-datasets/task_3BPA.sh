#!/bin/sh
#SBATCH --partition=a100
#SBATCH --job-name=MACE-3BPA
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=16
#SBATCH --gres=gpu:1


python3 /share/home/husiyu/software/MACE/mace/mace/cli/run_train.py \
  --name="MACE" \
  --train_file="/share/home/husiyu/software/MACE/data/BOTNet-datasets/dataset_3BPA/train_300K.xyz" \
  --valid_fraction=0.05 \
  --test_file="/share/home/husiyu/software/MACE/data/BOTNet-datasets/dataset_3BPA/test_300K.xyz" \
  --E0s='{1:-13.663181292231226, 6:-1029.2809654211628, 7:-1484.1187695035828, 8:-2042.0330099956639}' \
  --model="ScaleShiftMACE" \
  --hidden_irreps='32x0e' \
  --r_max=4.0 \
  --batch_size=20 \
  --max_num_epochs=100 \
  --ema \
  --ema_decay=0.99 \
  --amsgrad \
  --default_dtype="float32" \
  --device=cuda \
  --seed=123 \
  --swa



