from ase.io import read
import numpy as np

def MAE(file):
    print(file)
    configs = read(f'tests/{file}.xyz', index=':')
    diff_E = [ config.info['energy'] - config.info['MACE_energy'] for config in configs ]
    diff_F = [ config.arrays['forces'] - config.arrays['MACE_forces'] for config in configs ]
    print(f'MAE E: {np.mean(np.abs(diff_E)) * 1000:.1f} meV')
    print(f'MAE F: {np.mean(np.abs(diff_F)) * 1000:.1f} meV/Å\n')

MAE('aspirin_test')
MAE('paracetamol_test')
MAE('L2_aspirin_test')
MAE('L2_paracetamol_test')