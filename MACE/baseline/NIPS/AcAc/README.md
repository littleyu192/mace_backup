# AcAc

## 数据集

https://github.com/davkovacs/BOTNet-datasets

## 相关文献

https://arxiv.org/abs/2205.06643 

## 训练

训练使用的脚本为：[run.sh](./run.sh)

训练仅在 300K 的数据集中进行，测试集包括 300K 600K。

## 测试

[eval_configs.sh](./eval_configs.sh) 使用训练好的模型在测试集上进行 Energy 和 Force 的计算，结果存入 tests/ 。

使用 [plot.ipynb](./plot.ipynb) 中计算 RMSE 的脚本得到在测试集中的结果如下 Energy (E, meV), Force (F, meV/Å)。

|           |    *NequIP*     |     *MACE*     | MACE |
| :-------: | :-------------: | :------------: | :--: |
| 300K,   E | **0.81** (0.04) |   0.9 (0.03)   | 0.8  |
| 300K,   F |   5.90 (0.38)   | **5.1** (0.10) | 5.9  |
| 600K,   E |   6.04 (1.26)   | **4.6** (0.3)  | 8.2  |
| 600K,   F |   27.8 (3.29)   | **22.4** (0.9) | 26.7 |

表格中斜体标题是论文给出的参考结果。
