from ase.io import read
import numpy as np

configs1 = read(f'./dataset/test.xyz', index=':')
configs2 = read(f'./tests/test.xyz', index=':')
diff_E = [ config1.get_potential_energy() - config2.info['MACE_energy'] for config1, config2 in zip(configs1, configs2) ]
diff_E_per_atom = [ diff / len(config) for diff, config in zip(diff_E, configs1) ]
diff_F = [ config1.get_forces() - config2.arrays['MACE_forces'] for config1, config2 in zip(configs1, configs2) ]
diff_F = np.concatenate(diff_F)
print(f'RMSE E: {np.sqrt(np.mean(np.square(diff_E))) * 1000:.1f} meV; {np.sqrt(np.mean(np.square(diff_E_per_atom))) * 1000:.1f} meV/atom')
print(f'RMSE F: {np.sqrt(np.mean(np.square(diff_F))) * 1000:.1f} meV/Å')
print(f'MAE E: {np.mean(np.abs(diff_E)) * 1000:.1f} meV; {np.mean(np.abs(diff_E_per_atom)) * 1000:.1f} meV/atom')
print(f'MAE F: {np.mean(np.abs(diff_F)) * 1000:.1f} meV/Å')