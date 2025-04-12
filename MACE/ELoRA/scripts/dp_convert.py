import dpdata
from ase.io import read, write
import os

pathlist = [
]

for path in pathlist:
    data = dpdata.LabeledSystem(
        os.path.join("./", path),
        fmt="deepmd/npy",
    )
    print("# the data contains %d frames" % (len(data)))
    data.to_ase_traj("data.traj")

    atoms = read("data.traj", index=":")
    for atom in atoms:
        atom.calc.results["stress"] = None
    write("data.xyz", atoms, append=True)

    os.remove("data.traj")
