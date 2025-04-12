from ase.io import read
init_conf = read('./dataset/LiMnO2.cif', '0')
init_conf = init_conf * (2, 2, 2)
init_conf.write('./dataset/LiMnO2_222.cif')