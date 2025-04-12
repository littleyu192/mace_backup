import numpy as np
import os

def load_and_split_data(file_path, train_size=50, val_size=950):
    """
    Load the dataset and split it into training, validation, and test sets.
    """
    # Load the npz file
    data = np.load(file_path)
    
    # Extract arrays
    nuclear_charges = data["nuclear_charges"]
    coords = data["coords"]
    energies = data["energies"] * 0.04336410390059322  # Convert from kal/mol to eV
    forces = data["forces"] * 0.04336410390059322  # Convert from kal/mol/Angstrom to eV/Angstrom
    
    # Determine dataset size
    size = coords.shape[0]
    
    # Set random seed
    np.random.seed(123)
    
    # Generate and shuffle indices
    indices = np.arange(size)
    np.random.shuffle(indices)
    
    # Split the shuffled indices
    train_indices = indices[:train_size]
    val_indices = indices[train_size:train_size + val_size]
    test_indices = indices[train_size + val_size:]
    
    train_data = {
        "nuclear_charges": nuclear_charges,
        "coords": coords[train_indices],
        "energies": energies[train_indices],
        "forces": forces[train_indices],
    }
    val_data = {
        "nuclear_charges": nuclear_charges,
        "coords": coords[val_indices],
        "energies": energies[val_indices],
        "forces": forces[val_indices],
    }
    test_data = {
        "nuclear_charges": nuclear_charges,
        "coords": coords[test_indices],
        "energies": energies[test_indices],
        "forces": forces[test_indices],
    }
    
    return train_data, val_data, test_data

def nuclear_charge_to_atom_type(nuclear_charge):
    """
    Convert nuclear charge to atom type.
    """
    atom_map = {1: "H", 6: "C", 7: "N", 8: "O"}
    return atom_map.get(nuclear_charge, "Unknown")

def save_to_etxyz(data, output_file):
    """
    Save the dataset to an etxyz format file.
    """
    nuclear_charges = data["nuclear_charges"]
    coords = data["coords"]
    energies = data["energies"]
    forces = data["forces"]
    
    with open(output_file, "w") as f:
        for i in range(coords.shape[0]):  # Iterate through each sample
            n_atoms = nuclear_charges.shape[0]
            energy = energies[i]
            f.write(f"{n_atoms}\n")
            f.write(f'Properties=species:S:1:pos:R:3:forces:R:3 energy={energy:.8f} pbc="F F F"\n')
            for j in range(n_atoms):
                atom_type = nuclear_charge_to_atom_type(nuclear_charges[j])
                x, y, z = coords[i, j]
                fx, fy, fz = forces[i, j]
                f.write(f"{atom_type} {x:.8f} {y:.8f} {z:.8f} {fx:.8f} {fy:.8f} {fz:.8f}\n")


npz_dir = "rmd17/npz_data"
for file_name in os.listdir(npz_dir):
    molecule_name = file_name.split("_")[1].split(".")[0]
    train_data, val_data, test_data = load_and_split_data(os.path.join(npz_dir, file_name))
    os.makedirs(f"{molecule_name}/dataset/", exist_ok=True)
    save_to_etxyz(train_data, f"{molecule_name}/dataset/train.xyz")
    save_to_etxyz(val_data, f"{molecule_name}/dataset/valid.xyz")
    save_to_etxyz(test_data, f"{molecule_name}/dataset/test.xyz")