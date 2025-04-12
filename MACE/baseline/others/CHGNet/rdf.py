from ase.io import read
from ase.geometry.analysis import Analysis
import numpy as np
import matplotlib.pyplot as plt

configs = read('./test/md.xyz', index=':')
rmax = 2.755514547094113
nbins = 100
rdf = np.sum(Analysis(configs).get_rdf(rmax=rmax, nbins=nbins), axis=0) / len(configs)
plt.plot(np.linspace(0, rmax, nbins), rdf, label='Li-Li')
rdf = np.sum(Analysis(configs).get_rdf(rmax=rmax, nbins=nbins, elements=[3,27]), axis=0) / len(configs)
plt.plot(np.linspace(0, rmax, nbins), rdf, label='Li-Co')
rdf = np.sum(Analysis(configs).get_rdf(rmax=rmax, nbins=nbins, elements=[3,8]), axis=0) / len(configs)
plt.plot(np.linspace(0, rmax, nbins), rdf, label='Li-O')
plt.title('Radial distribution function')
plt.xlabel('r (Å)')
plt.ylabel('g(r)')
plt.legend()
plt.savefig('rdf.png')