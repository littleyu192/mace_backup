from ase.io import read
import numpy as np

configs = read(f'./tests/test.xyz', index=':')
diff_E = [ config.info['energy'] - config.info['MACE_energy'] for config in configs ]
diff_E_per_atom = [ diff / len(config) for diff, config in zip(diff_E, configs) ]
diff_F = [ config.arrays['forces'] - config.arrays['MACE_forces'] for config in configs ]
print(f'RMSE E: {np.sqrt(np.mean(np.square(diff_E))) * 1000:.1f} meV; {np.sqrt(np.mean(np.square(diff_E_per_atom))) * 1000:.1f} meV/atom')
print(f'RMSE F: {np.sqrt(np.mean(np.square(diff_F))) * 1000:.1f} meV/Å')
print(f'MAE E: {np.mean(np.abs(diff_E)) * 1000:.1f} meV; {np.mean(np.abs(diff_E_per_atom)) * 1000:.1f} meV/atom')
print(f'MAE F: {np.mean(np.abs(diff_F)) * 1000:.1f} meV/Å')