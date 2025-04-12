# scripts

- [dp_convert.py](./dp_convert.py) 将 deepmd 格式的文件转换为 xyz 格式

- [loss.py](./loss.py) 绘制 loss 曲线

- [eval_configs.sh](./eval_configs.sh) 用训练好的模型进行推理

- [error.py](./error.py) 从推理出的数据计算 RMSE 和 MAE

- [error2.py](./error.py) 如果 ase 版本较高，会导致推理结果中不包含原始 dft 能量，这时需要从原文件中读取能量