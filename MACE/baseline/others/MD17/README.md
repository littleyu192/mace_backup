# 数据集

http://www.sgdml.org/

# 预处理

使用 [convert.py](./convert.py) 向文件中添加能量、坐标、力的格式描述。

使用 [spilt.py](./spilt.py) 转换单位、打乱并拆分出 1000 个样本作为训练集。

# 训练

训练使用的脚本为：[run_aspirin.sh](./run_aspirin.sh)  [run_paracetamol.sh](./run_paracetamol.sh)

训练仅在随机抽取的 1000 个样本的数据集中进行，测试集为其余样本。

# 测试

[eval_configs_aspirin.sh](./eval_configs_aspirin.sh)  [eval_configs_paracetamol.sh](./eval_configs_aspirin.sh) 使用训练好的模型在测试集上进行 Energy 和 Force 的计算。

使用 [mae.py](./mae.py) 中计算 MAE 的脚本得到在测试集中的结果如下 Energy (E, meV), Force (F, meV/Å)。

|                        | *NequIP* | *MACE*  | MACE |
| :--------------------: | :------: | :-----: | :--: |
| Aspirin,             E |   2.3    | **2.2** | 5.6  |
| Aspirin,             F |   8.2    | **6.6** | 7.0  |
|    Paracetamol,   E    |   1.4    | **1.3** | 5.0  |
|    Paracetamol,   F    |   5.9    | **4.8** | 5.2  |

注意：表格中斜体标题是论文给出的 **rMD17** 的参考结果，和 **MD17** 的结果 **不具有可比性**。
