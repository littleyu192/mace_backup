import re
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator


def plot_stress(filename, axs, name):
    # 初始化空列表来存储数据
    epochs = []
    losses = []
    mae_e_per_atom = []
    mae_f = []
    mae_stress_per_atom = []
    
    # 读取日志文件
    with open(filename, 'r') as file:
        for line in file:
            # 使用正则表达式匹配并提取数据
            match = re.search(
                r'Epoch (\d+): loss=([0-9.]+), MAE_E_per_atom=([0-9.]+) meV, MAE_F=([0-9.]+) meV / A, MAE_stress_per_atom=([0-9.]+) meV / A\^3',
                line)
            if match:
                epoch = int(match.group(1))
                loss = float(match.group(2)) * 32
                mae_e = float(match.group(3))
                mae_f_value = float(match.group(4))
                mae_stress = float(match.group(5))
    
                epochs.append(epoch)
                losses.append(loss)
                mae_e_per_atom.append(mae_e)
                mae_f.append(mae_f_value)
                mae_stress_per_atom.append(mae_stress)
    
    # 绘制 loss 随 epoch 变化的图
    axs[0][0].plot(epochs, losses, label=name)

    # 绘制 MAE_E_per_atom 随 epoch 变化的图
    axs[0][1].plot(epochs, mae_e_per_atom, label=name)

    # 绘制 MAE_F 随 epoch 变化的图
    axs[1][0].plot(epochs, mae_f, label=name)

    # 绘制 MAE_stress_per_atom 随 epoch 变化的图
    axs[1][1].plot(epochs, mae_stress_per_atom, label=name)

        

# 创建子图
fig, axs = plt.subplots(2, 2, figsize=(9, 6))

plot_stress('logs/L0_ustc_2node.log',axs,'small')
plot_stress('logs/L1_ustc_2node.log',axs,'medium')
plot_stress('logs/L2_ustc_4node.log',axs,'large')
plot_stress('logs/L1_ustc_2node_2.log',axs,'medium_retry')
plot_stress('logs/L0_dcu_2node.log',axs,'small_dcu')

axs[0][0].set_xlabel('Epoch')
axs[0][0].set_ylabel('Loss')
axs[0][0].legend()
axs[0][0].set_xlim(0, 250)
axs[0][0].set_ylim(0, 0.0175)
axs[0][0].yaxis.set_major_locator(MultipleLocator(0.0025))
axs[0][0].grid(True)

axs[0][1].set_xlabel('Epoch')
axs[0][1].set_ylabel('MAE_E_per_atom (meV)')
axs[0][1].legend()
axs[0][1].set_xlim(0, 250)
axs[0][1].set_ylim(0, 200)
axs[0][1].yaxis.set_major_locator(MultipleLocator(50))
axs[0][1].grid(True)

axs[1][0].set_xlabel('Epoch')
axs[1][0].set_ylabel('MAE_F (meV / A)')
axs[1][0].legend()
axs[1][0].set_xlim(0, 250)
axs[1][0].set_ylim(0, 120)
axs[1][0].yaxis.set_major_locator(MultipleLocator(20))
axs[1][0].grid(True)

axs[1][1].set_xlabel('Epoch')
axs[1][1].set_ylabel('MAE_stress_per_atom (meV / A^3)')
axs[1][1].legend()
axs[1][1].set_xlim(0, 250)
axs[1][1].set_ylim(0, 0.35)
axs[1][1].yaxis.set_major_locator(MultipleLocator(0.1))
axs[1][1].grid(True)

# 自动调整子图间距
plt.tight_layout()

# 显示图表
plt.savefig("loss.png")
