from ase.io import read
import numpy as np

def RMSE(path, type):
    print(f'{path} {type}')
    configs_origin = read(f'dataset/test_{type}.xyz', index=':')
    configs = read(f'{path}/tests/test_{type}.xyz', index=':')
    diff_E = [ config_origin.get_potential_energy() - config.info['MACE_energy'] for config_origin, config in zip(configs_origin, configs) ]
    diff_F = [ config_origin.get_forces() - config.arrays['MACE_forces'] for config_origin, config in zip(configs_origin, configs) ]
    print(f'RMSE E: {np.sqrt(np.mean(np.square(diff_E))) * 1000:.1f} meV')
    print(f'RMSE F: {np.sqrt(np.mean(np.square(diff_F))) * 1000:.1f} meV/Å\n')
    return np.sqrt(np.mean(np.square(diff_E))) * 1000, np.sqrt(np.mean(np.square(diff_F))) * 1000

for type in ['MD_300K', 'MD_600K']:
    LoRA_123 = RMSE("LoRA_123", type)
    LoRA_42 = RMSE("LoRA_42", type)
    LoRA_2024 = RMSE("LoRA_2024", type)
    finetune_123 = RMSE("finetune_123", type)
    finetune_42 = RMSE("finetune_42", type)
    finetune_2024 = RMSE("finetune_2024", type)
    LoRA_mean = np.mean([LoRA_123, LoRA_42, LoRA_2024], axis=0)
    LoRA_std = np.std([LoRA_123, LoRA_42, LoRA_2024], axis=0)
    finetune_mean = np.mean([finetune_123, finetune_42, finetune_2024], axis=0)
    finetune_std = np.std([finetune_123, finetune_42, finetune_2024], axis=0)
    print(f'{type} results:')
    print(f'LoRA mean: E {LoRA_mean[0]:.1f} meV, F {LoRA_mean[1]:.1f} meV/Å')
    print(f'LoRA std: E {LoRA_std[0]:.2f} meV, F {LoRA_std[1]:.2f} meV/Å')
    print(f'finetune mean: E {finetune_mean[0]:.1f} meV, F {finetune_mean[1]:.1f} meV/Å')
    print(f'finetune std: E {finetune_std[0]:.2f} meV, F {finetune_std[1]:.2f} meV/Å')
