

# PACE

## Requirements:

Python >= 3.8;

PyTorch >= 1.11 .

## Baseline (Full Training / Full Parameter Fine-tuning)

Use the code from the [`husiyu/PACE_baseline`](https://github.com/divelab/AIRS/tree/main/OpenMol/PACE) branch, This branch is based on commit [dd0a772](https://github.com/divelab/AIRS/commit/dd0a772e90730719855e0ce3993d2489cb274b70) from [AIRS/OpenMol/PACE](https://github.com/divelab/AIRS/tree/main/OpenMol/PACE) .

**Usage**:  
Install dependencies according to the README's Installation section, then install the PACE library from the [`husiyu/PACE_baseline`](https://github.com/divelab/AIRS/tree/main/OpenMol/PACE) branch source code.

```
# Create conda environment and activate
conda create --name pace_baseline python=3.8
conda activate pace_baseline

# Install PyTorch
conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3 -c pytorch

# (optional) Install PACE's dependencies from Conda as well
conda install numpy scipy matplotlib ase opt_einsum prettytable pandas e3nn 

# install the requirements
pip install e3nn torch-ema prettytable ase==3.22.1

# Clone and install PACE (and all required packages)
pip install git+https://github.com/littleyu192/mace_backup@husiyu/PACE_baseline
```
## E3nn LoRA

Use the code from the [`zhujie/PACE_LoRA`](https://github.com/littleyu192/mace_backup/tree/zhujie/PACE_LoRA) branch. This branch adds ELoRA (Efficient Low-Rank Adaptation) to `husiyu/PACE_baseline`.

**Usage**:  
1. Install dependencies according to the standard Installation instructions (**excluding e3nn**)  
2. **Install modified e3nn with ELoRA support**  
3. Install PACE from the `PACE_LoRA` branch source code

```
# Create conda environment and activate
conda create -n pace_lora python=3.8
conda activate pace_lora

# Install PyTorch
conda install pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3 -c pytorch

# (optional) Install PACE's dependencies from Conda as well
conda install numpy scipy matplotlib ase opt_einsum prettytable pandas

# install the requirements
pip install e3nn torch-ema prettytable ase==3.22.1

# Clone and install e3nn with ELoRA
pip install git+https://github.com/littleyu192/mace_backup@wangchen/e3nn

# Clone and install PACE (and all required packages)
pip install git+https://github.com/littleyu192/mace_backup@zhujie/PACE_lora

```

## Adapter

Use the code from the [`husiyu/PACE_adapter`](https://github.com/divelab/AIRS/tree/main/OpenMol/PACE) branch. This branch adds Adapter modules to `PACE_baseline`.

**Usage**:  
Install dependencies according to the standard Installation instructions, then install PACE from the `PACE_adapter` branch source code.

---

## Readout

Use the code from the [`husiyu/PACE_readout`](https://github.com/divelab/AIRS/tree/main/OpenMol/PACE) branch. This branch modifies `PACE_baseline` to make **only the readout layers trainable**.

**Usage**:  
Install dependencies per the standard Installation instructions, then install PACE from the `PACE_readout` branch source code.

---

## Training
Baseline and LoRA share the same command-line interface and training scripts. To reproduce different results, simply switch the active conda environment (e.g., pace_baseline or pace_lora) before running the training commands.

```bash
module load conda/3-2020.07 cudnn/12 gcc/11.4.0
source activate pace

python main_rmd17.py --device $DEVICE --task task_name --output_dir ./results/pace/aspirin --num_bessel 6
```

task_name is the task name, which is the name of each folder under the example folder, such as aspirin, aspirin_dft, Azobenzene, Benzene...

In addition, you need to change the raw_file_names function (about line 40) in the ./PACE/dataset/PygMD17.py file, whose output is the corresponding input file path;

The root of the train_dataset/valid_dataset/test_dataset in the main_rmd17~.py file is the path where the data files are stored or loaded.

LORA：
```bash
module load conda/3-2020.07 cudnn/12 gcc/11.4.0
source activate pace_lora

python main_rmd17_lora.py --device $DEVICE --task task_name --output_dir ./results/pace/aspirin --num_bessel 6  --continue_run
```

You also need to modify the checkpoint path (line 200 of main_rmd17_lora.py)

## Important Notes


---

## Reference

[1] Batatia, Ilyes, et al. "MACE: Higher order equivariant message passing neural networks for fast and accurate force fields." *Advances in neural information processing systems* 35 (2022): 11423-11436.

























