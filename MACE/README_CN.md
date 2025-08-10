# MACE

## baseline（从头训练/全参数微调）

使用 `MACE_baseline` 分支代码。该分支代码基于 https://github.com/ACEsuit/mace (commit hash: 346a829f)，进行了以下修改：

- 将分布式训练环境从 Slurm 改为 torchrun
- 增加 EnergyForcesLoss （与论文 [1] 设置对齐）

使用时按照 README 中 Installation 部分先安装各项依赖，然后将安装 MACE 库的部分改为从 `MACE_baseline` 分支的源码安装。

## ELoRA

使用 `MACE_ELoRA` 分支代码。该分支代码在 `MACE_baseline` 分支代码的基础上添加了 ELoRA。

使用时按照 README 中 Installation 部分先安装各项依赖（除了 e3nn），然后**单独安装添加了 ELoRA 的 e3nn**，最后将安装 MACE 库的部分改为从 `MACE_ELoRA` 分支的源码安装。

## Adapter

使用 `MACE_adapter` 分支代码。该分支代码在 `MACE_baseline` 分支代码的基础上添加了 Adapter。

使用时按照 README 中 Installation 部分先安装各项依赖，然后将安装 MACE 库的部分改为从 `MACE_adapter` 分支的源码安装。

## Readout

使用 `MACE_readout` 分支代码。该分支代码在 `MACE_baseline` 分支代码的基础上只使 readout 层参数可以训练。

使用时按照 README 中 Installation 部分先安装各项依赖，然后将安装 MACE 库的部分改为从 `MACE_readout` 分支的源码安装。

## 注意

1. 在使用 `MACE_baseline` `MACE_adapter` `MACE_readout`代码时需要使用**官方版本**的 e3nn。

2. 在使用 `MACE_ELoRA` 代码时需要使用**修改后**的 e3nn。

3. 不同微调方法只需要配置不同的环境，不需要修改脚本。

4. 无机数据集微调使用 [2024-01-07-mace-128-L2_epoch-199.model](https://github.com/ACEsuit/mace-foundations/releases/download/mace_mp_0/2024-01-07-mace-128-L2_epoch-199.model)

5. 有机数据集微调使用 [MACE-OFF23_medium.model](https://github.com/ACEsuit/mace-off/blob/main/mace_off23/MACE-OFF23_medium.model)

## 参考文献

[1] Batatia, Ilyes, et al. "MACE: Higher order equivariant message passing neural networks for fast and accurate force fields." *Advances in neural information processing systems* 35 (2022): 11423-11436.