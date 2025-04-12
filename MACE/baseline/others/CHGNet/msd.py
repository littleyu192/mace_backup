import numpy as np
from ase.io import read
import matplotlib.pyplot as plt

def calculate_msd(trajectory, element):
    n_steps = len(trajectory)
    
    # element 对应原子的 index
    element_indices = np.where(trajectory[0].numbers == element)[0]
    initial_positions = trajectory[0].get_positions()[element_indices]
    
    # 遍历时间步长
    current_positions = [trajectory[step].get_positions()[element_indices] for step in range(n_steps)]
    displacements = current_positions - initial_positions
    squared_displacements = displacements ** 2
    msd = np.mean(np.sum(squared_displacements, axis=2), axis=1)
    
    return msd

# 读取轨迹文件
trajectory = read('./test/md.xyz', index=':')

# 计算MSD
msd_values = calculate_msd(trajectory, 3)
time_steps = np.arange(len(msd_values))

# 可视化MSD随时间的变化
plt.plot(time_steps, msd_values)
plt.xlabel('Time step')
plt.ylabel('MSD (Å^2)')
plt.title('Mean Squared Displacement')
plt.savefig("./msd.png")
