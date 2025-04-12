import re
import matplotlib.pyplot as plt

def plot(filename, axs, name, max_epoch=None):
    epoch = []
    loss = []
    rmse_e = []
    rmse_f = []
    
    with open(filename, 'r') as file:
        for line in file:
            match = re.search(
                r'Epoch (\d+): loss=([0-9.]+), RMSE_E=([0-9.]+) meV, RMSE_F=([0-9.]+) meV / A',
                line)
            if match and (max_epoch is None or int(match.group(1)) < max_epoch):
                epoch.append(int(match.group(1)))
                loss.append(float(match.group(2)))
                rmse_e.append(float(match.group(3)))
                rmse_f.append(float(match.group(4)))
    
    axs[0].plot(epoch, loss, label=name)
    axs[1].plot(epoch, rmse_e, label=name)
    axs[2].plot(epoch, rmse_f, label=name)
        

import os
for name in os.listdir('.'):
    if os.path.isdir(name):
        if 'dataset' in os.listdir(name):
            fig, axs = plt.subplots(1, 3, figsize=(15, 5))

            plot(f'./{name}/finetune/logs/{name}_run-123.log',axs,'finetune')
            plot(f'./{name}/LoRA/logs/{name}_run-123.log',axs,'LoRA')

            axs[0].set_xlabel('Epoch')
            axs[0].set_ylabel('Loss')
            axs[0].set_yscale('log')
            axs[0].legend()
            axs[0].grid(True)

            axs[1].set_xlabel('Epoch')
            axs[1].set_ylabel('RMSE E(meV)')
            axs[1].set_yscale('log')
            axs[1].legend()
            axs[1].grid(True)

            axs[2].set_xlabel('Epoch')
            axs[2].set_ylabel('RMSE F(meV/A)')
            axs[2].set_yscale('log')
            axs[2].legend()
            axs[2].grid(True)

            plt.suptitle(name)
            plt.tight_layout()
            plt.savefig(f"./{name}/loss.png")