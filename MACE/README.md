# MACE pretrained model

## Requirements:

Python >= 3.7;

PyTorch >= 1.12 (training with float64 is not supported with PyTorch 2.1 but is supported with 2.2 and later.).

## Baseline (Full Training / Full Parameter Fine-tuning)

Use the code from the [`wangchen/MACE_baseline`](https://github.com/ACEsuit/mace) branch. This branch is based on commit [346a829f](https://github.com/ACEsuit/mace/commit/346a829f) from [ACEsuit/mace](https://github.com/ACEsuit/mace) with the following modifications:

- Replaced Slurm-based distributed training with torchrun
- Added `EnergyForcesLoss` (aligned with settings in paper [[1]](#reference))

**Usage**:  
Install dependencies according to the README's Installation section, then install the MACE library from the [`wangchen/MACE_baseline`]（https://github.com/littleyu192/mace_backup/tree/wangchen/MACE_baseline） branch source code.

```
# Create conda environment and activate
conda create --name mace_baseline
conda activate mace_baseline

# Install PyTorch
conda install pytorch torchvision torchaudio pytorch-cuda=11.6 -c pytorch -c nvidia

# (optional) Install MACE's dependencies from Conda as well
conda install numpy scipy matplotlib ase opt_einsum prettytable pandas e3nn

# Clone and install MACE (and all required packages)
pip install git+https://github.com/littleyu192/mace_backup@wangchen/MACE_baseline
```
## E3nn LoRA

Use the code from the [`wangchen/MACE_ELoRA`](https://github.com/littleyu192/mace_backup/tree/wangchen/MACE_ELoRA) branch. This branch adds ELoRA (Efficient Low-Rank Adaptation) to `wangchen/MACE_baseline`.

**Usage**:  
1. Install dependencies according to the standard Installation instructions (**excluding e3nn**)  
2. **Install modified e3nn with ELoRA support**  
3. Install MACE from the `MACE_ELoRA` branch source code

```
# Create conda environment and activate
conda create -n mace_elora python=3.10
conda activate mace_elora

# Install PyTorch
conda install pytorch torchvision torchaudio pytorch-cuda=11.6 -c pytorch -c nvidia

# (optional) Install MACE's dependencies from Conda as well
conda install numpy scipy matplotlib ase opt_einsum prettytable pandas

# Clone and install e3nn with ELoRA
pip install git+https://github.com/littleyu192/mace_backup@wangchen/e3nn

# Clone and install MACE with ELoRA (and all required packages)
pip install git+https://github.com/littleyu192/mace_backup@wangchen/MACE_ELoRA
```

## Adapter

Use the code from the [`wangchen/MACE_adapter`](https://github.com/littleyu192/mace_backup/tree/wangchen/MACE_adapter) branch. This branch adds Adapter modules to `MACE_baseline`.

**Usage**:  
Install dependencies according to the standard Installation instructions, then install MACE from the `MACE_adapter` branch source code.

---

## Readout

Use the code from the [`wangchen/MACE_readout`](https://github.com/littleyu192/mace_backup/tree/wangchen/MACE_readout) branch. This branch modifies `MACE_baseline` to make **only the readout layers trainable**.

**Usage**:  
Install dependencies per the standard Installation instructions, then install MACE from the `MACE_readout` branch source code.

---

## Training
Baseline and ELoRA share the same command-line interface and training scripts. To reproduce different results, simply switch the active conda environment (e.g., mace_baseline or mace_elora) before running the training commands.

Inorganic dataset:
```
mace_run_train \
    --name="MACE_model" \
    --train_file="./dataset/train.xyz" \
    --valid_file="./dataset/valid.xyz" \
    --E0s="average" \
    --foundation_model="2024-01-07-mace-128-L2_epoch-199.model" \
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
    --batch_size=5 \
    --valid_batch_size=5 \
    --lr_factor=0.8 \
    --scheduler_patience=5 \
    --ema \
    --ema_decay=0.995 \
    --max_num_epochs=200 \
    --error_table="TotalRMSE" \
    --device=cuda \
    --seed=123 \
    --clip_grad=100 \
    --save_cpu 
```
Organic dataset:
```
mace_run_train \
    --name="MACE_model" \
    --train_file="./dataset/train.xyz" \
    --valid_fraction=0.1 \
    --test_file="./dataset/test.xyz" \
    --E0s='average' \
    --foundation_model="MACE-OFF23_medium.model" \
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
    --save_cpu 
```

## Important Notes

1. For `MACE_baseline`, `MACE_adapter`, and `MACE_readout`: Use the **[official e3nn library](https://github.com/e3nn/e3nn)**  
2. For `MACE_ELoRA`: Use the **[modified e3nn](https://github.com/e3nn/e3nn/tree/ELoRA_branch)** version  
3. **No script modifications needed** for different fine-tuning approaches - just switch environments  
4. **Inorganic dataset fine-tuning**: Use pre-trained model [2024-01-07-mace-128-L2_epoch-199.model](https://github.com/ACEsuit/mace-foundations/releases/download/mace_mp_0/2024-01-07-mace-128-L2_epoch-199.model)  
5. **Organic dataset fine-tuning**: Use pre-trained model [MACE-OFF23_medium.model](https://github.com/ACEsuit/mace-off/blob/main/mace_off23/MACE-OFF23_medium.model)  

---

## Reference

[1] Batatia, Ilyes, et al. "MACE: Higher order equivariant message passing neural networks for fast and accurate force fields." *Advances in neural information processing systems* 35 (2022): 11423-11436.
