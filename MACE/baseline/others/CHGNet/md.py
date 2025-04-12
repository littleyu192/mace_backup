from ase import units
from ase.md.nvtberendsen import NVTBerendsen
from ase.md.npt import NPT
from ase.md.verlet import VelocityVerlet
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.io import read
from ase.md import MDLogger

from mace.calculators import MACECalculator

calculator = MACECalculator(model_paths='../MPtrj/L2.model', device='cuda')
init_conf = read('./dataset/Li9Co7O16.cif', '0')
init_conf.set_calculator(calculator)
MaxwellBoltzmannDistribution(init_conf, temperature_K=1800)

def write_frame():
    dyn.atoms.write('./test/md.xyz', append=True)

# dyn = VelocityVerlet(init_conf, 1*units.fs)
# dyn.attach(MDLogger(dyn, dyn.atoms, './md/md.log'), interval=1)
# dyn.attach(write_frame, interval=1)
# dyn.run(2000)

dyn = NVTBerendsen(init_conf, 1*units.fs, temperature_K=1800, taut=0.1*1000*units.fs)
# dyn = NPT(init_conf, 1*units.fs, temperature_K=1800, externalstress=0, ttime=10*units.fs, pfactor=None)
dyn.attach(MDLogger(dyn, dyn.atoms, './test/md.log'), interval=1)
dyn.attach(write_frame, interval=1)
dyn.run(1500)

print("MD finished!")