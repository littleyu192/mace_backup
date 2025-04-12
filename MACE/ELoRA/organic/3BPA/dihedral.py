# from ase.io import read
# import numpy as np

# def RMSE(path, type):
#     print(f'{type}')
#     configs_origin = read(f'/home/bingxing2/home/scx9kv2/opt/mace/tasks/3BPA/dataset/test_{type}.xyz', index=':')
#     configs = read(f'{path}/tests/test_{type}.xyz', index=':')
#     diff_E = [ config_origin.get_potential_energy() - config.info['MACE_energy'] for config_origin, config in zip(configs_origin, configs) ]
#     diff_F = [ config_origin.get_forces() - config.arrays['MACE_forces'] for config_origin, config in zip(configs_origin, configs) ]
#     print(f'RMSE E: {np.sqrt(np.mean(np.square(diff_E))) * 1000:.1f} meV')
#     print(f'RMSE F: {np.sqrt(np.mean(np.square(diff_F))) * 1000:.1f} meV/Å\n')

# for type in ['300K', '600K', '1200K', 'dih']:
#     RMSE("LoRA_123", type)
#     RMSE("LoRA_42", type)
#     RMSE("LoRA_2024", type)
#     RMSE("baseline_123", type)
#     RMSE("baseline_42", type)
#     RMSE("baseline_2024", type)

from ase.io import read
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["text.usetex"] = True
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["font.family"] = "Times New Roman"


def dihedral(alpha, beta, axes):
    def plot(axes, method, min_energy, color, name):
        configs_42 = read(f"{method}_42/tests/test_dih.xyz", index=":")
        config_alpha_beta_42 = []
        for config in configs_42:
            if (
                config.info["dihedrals"][0] == alpha
                and config.info["dihedrals"][1] == beta
            ):
                config_alpha_beta_42.append(config)
        MACE_energy_42 = [config.info["MACE_energy"] for config in config_alpha_beta_42]
        MACE_energy_42 = (MACE_energy_42 - min_energy) * 1000
        dihedrals = [config.info["dihedrals"][2] for config in config_alpha_beta_42]

        configs_123 = read(f"{method}_123/tests/test_dih.xyz", index=":")
        config_alpha_beta_123 = []
        for config in configs_123:
            if (
                config.info["dihedrals"][0] == alpha
                and config.info["dihedrals"][1] == beta
            ):
                config_alpha_beta_123.append(config)
        MACE_energy_123 = [
            config.info["MACE_energy"] for config in config_alpha_beta_123
        ]
        MACE_energy_123 = (MACE_energy_123 - min_energy) * 1000

        configs_2024 = read(f"{method}_2024/tests/test_dih.xyz", index=":")
        config_alpha_beta_2024 = []
        for config in configs_2024:
            if (
                config.info["dihedrals"][0] == alpha
                and config.info["dihedrals"][1] == beta
            ):
                config_alpha_beta_2024.append(config)
        MACE_energy_2024 = [
            config.info["MACE_energy"] for config in config_alpha_beta_2024
        ]
        MACE_energy_2024 = (MACE_energy_2024 - min_energy) * 1000

        MACE_energy_avg = (MACE_energy_42 + MACE_energy_123 + MACE_energy_2024) / 3
        MACE_energy_std = np.std(
            [MACE_energy_42, MACE_energy_123, MACE_energy_2024], axis=0
        )

        axes.plot(dihedrals, MACE_energy_avg, label=name, color=color, linewidth=2)
        axes.fill_between(
            dihedrals,
            MACE_energy_avg - MACE_energy_std,
            MACE_energy_avg + MACE_energy_std,
            alpha=0.2,
            color=color,
        )

    configs = read(
        "./dataset/test_dih.xyz",
        index=":",
    )
    config_alpha_beta = []
    for config in configs:
        if config.info["dihedrals"][0] == alpha and config.info["dihedrals"][1] == beta:
            config_alpha_beta.append(config)
    energy = [config.get_potential_energy() for config in config_alpha_beta]
    min_energy = np.min(energy)
    energy = (energy - min_energy) * 1000
    dihedrals = [config.info["dihedrals"][2] for config in config_alpha_beta]
    axes.plot(dihedrals, energy, label="DFT", color="black", linewidth=2)

    plot(axes, "baseline", min_energy, "tab:blue", "From scratch")
    plot(axes, "LoRA", min_energy, "tab:orange", "ELoRA")

    axes.set_xlabel("$\gamma$ ($^\circ$)", fontsize=15)
    axes.set_ylabel("$\Delta$E (meV)", fontsize=15)
    axes.legend(fontsize=12)
    axes.set_title(f"$\\alpha$ = ${alpha}^\circ$, $\\beta$ = ${beta}^\circ$", fontsize=15)
    axes.tick_params(axis='both', labelsize=12)


fig, axes = plt.subplots(1, 3, figsize=(16, 5))

dihedral(71.0, 120.0, axes[0])
dihedral(67.0, 150.0, axes[1])
dihedral(151.0, 180.0, axes[2])

plt.tight_layout()
plt.savefig("dihedral.pdf")
