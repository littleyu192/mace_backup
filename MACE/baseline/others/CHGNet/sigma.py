from ase.io import read
from ase.md.analysis import DiffusionCoefficient
import numpy as np

configs = read('./md/md.xyz', index='7000:')
diffusionCoefficient = DiffusionCoefficient(configs, 1, list(np.where(configs[0].numbers == 3)[0]))
diffusionCoefficient.calculate()
diffusionCoefficient_result = diffusionCoefficient.get_diffusion_coefficients()

# 利用扩散系数计算锂离子电导率
# 电导率的计算公式为：σ = n * e^2 * D / (k * T)
# n: 离子数密度，由离子数除以体积得到
# e: 电子电荷
# D: 扩散系数
# k: 玻尔兹曼常数
# T: 温度
n = len(np.where(configs[0].numbers == 3)[0]) / configs[0].get_volume() # 单位为 1/Å^3
n = n * 1e30 # 单位为 1/m^3
e = 1.60217662e-19 # 单位为 C
k = 1.38064852e-23 # 单位为 J/K
T = 300 # 单位为 K
D = diffusionCoefficient_result[0][0] # 单位为 Å^2/fs
D = D * 1e-20 / 1e-15 # 单位为 m^2/s
sigma = n * e**2 * D / (k * T) # 单位为 S/m
# 将单位转为 mS/cm
print('Li ion conductivity: %.3f mS/cm' % (sigma * 10))