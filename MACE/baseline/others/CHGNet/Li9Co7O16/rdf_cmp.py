from ase.io import read
from ase.geometry.analysis import Analysis
import numpy as np
import matplotlib.pyplot as plt

rmax = 2.755514547094113
nbins = 100

configs = read('./md.xyz', index=':')
rdf = np.sum(Analysis(configs).get_rdf(rmax=rmax, nbins=nbins), axis=0) / len(configs)
plt.plot(np.linspace(0, rmax, nbins), rdf, label='Li-Li(MACE)', color='blue')
rdf = np.sum(Analysis(configs).get_rdf(rmax=rmax, nbins=nbins, elements=[3,27]), axis=0) / len(configs)
plt.plot(np.linspace(0, rmax, nbins), rdf, label='Li-Co(MACE)', color='orange')
rdf = np.sum(Analysis(configs).get_rdf(rmax=rmax, nbins=nbins, elements=[3,8]), axis=0) / len(configs)
plt.plot(np.linspace(0, rmax, nbins), rdf, label='Li-O(MACE)', color='green')

configs = read('./vasp/mp-1175469-Li9Co7O16/aimd/XDATCAR', index=':')
rdf = np.sum(Analysis(configs).get_rdf(rmax=rmax, nbins=nbins), axis=0) / len(configs)
plt.plot(np.linspace(0, rmax, nbins), rdf, label='Li-Li(VASP)', color='blue', linestyle='--')
rdf = np.sum(Analysis(configs).get_rdf(rmax=rmax, nbins=nbins, elements=[3,27]), axis=0) / len(configs)
plt.plot(np.linspace(0, rmax, nbins), rdf, label='Li-Co(VASP)', color='orange', linestyle='--')
rdf = np.sum(Analysis(configs).get_rdf(rmax=rmax, nbins=nbins, elements=[3,8]), axis=0) / len(configs)
plt.plot(np.linspace(0, rmax, nbins), rdf, label='Li-O(VASP)', color='green', linestyle='--')

plt.title('Radial distribution function')
plt.xlabel('r (Å)')
plt.ylabel('g(r)')
plt.legend()
plt.savefig('rdf_cmp.png')


