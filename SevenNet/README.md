# SevenNet

## baseline（从头训练/全参数微调）

使用 `SevenNet_baseline` 分支代码。该分支代码基于 https://github.com/MDIL-SNU/SevenNet (commit hash: f981b7c)，进行了以下修改：

- 去除加载模型时对缺失参数的检查

使用时按照 README 中 Installation 部分先安装各项依赖，然后将安装 SevenNet 库的部分改为从 `SevenNet_baseline` 分支的源码安装。

## ELoRA

使用 `SevenNet_ELoRA` 分支代码。该分支代码在 `SevenNet_baseline` 分支代码的基础上添加了 ELoRA。

使用时按照 README 中 Installation 部分先安装各项依赖（除了 e3nn），然后**单独安装添加了 ELoRA 的 e3nn**，最后将安装 SevenNet 库的部分改为从 `SevenNet_ELoRA` 分支的源码安装。

## Adapter

使用 `SevenNet_adapter` 分支代码。该分支代码在 `SevenNet_baseline` 分支代码的基础上添加了 Adapter。

使用时按照 README 中 Installation 部分先安装各项依赖，然后将安装 SevenNet 库的部分改为从 `SevenNet_adapter` 分支的源码安装。

## Readout

使用 `SevenNet_readout` 分支代码。该分支代码在 `SevenNet_baseline` 分支代码的基础上只使 readout 层参数可以训练。

使用时按照 README 中 Installation 部分先安装各项依赖，然后将安装 SevenNet 库的部分改为从 `SevenNet_readout` 分支的源码安装。

## 注意

1. 在使用 `SevenNet_baseline` `SevenNet_adapter` `SevenNet_readout`代码时需要使用**官方版本**的 e3nn。

2. 在使用 `SevenNet_ELoRA` 代码时需要使用**修改后**的 e3nn。

3. 不同微调方法只需要配置不同的环境，不需要修改脚本。

4. 无机数据集微调使用 SevenNet-0。

5. 有机数据集没有对应的预训练模型，无法训练。

## 测试

|        | SevenNet (Full-parameter) | SevenNet (Adapter) | SevenNet (Readout) | SevenNet (ELoRA) |
| ------ | :-----------------------: | :----------------: | :----------------: | :--------------: |
| Cu,  E |            0.9            |        2.5         |        10.2        |     **0.8**      |
| Cu,  F |           12.8            |        32.1        |       153.2        |     **12.2**     |
| Sn,  E |            3.4            |        6.8         |        16.4        |     **3.0**      |
| Sn,  F |           74.1            |       117.0        |       190.5        |     **73.4**     |