import random
from ase.io import read, write
from ase.units import kcal, mol

db = read('./paracetamol.xyz', ':')
# energy 和 force 的单位分别是 kcal mol-1 和 kcal mol-1 Å-1
# 将其转换为 eV 和 eV Å-1
for atoms in db:
    atoms.calc.results['energy'] *= kcal/mol
    atoms.calc.results['forces'] *= kcal/mol
# 打乱数据集
random.seed(123)
random.shuffle(db)
train_db = db[:1000]
test_db = db[1000:]
write('./dataset/paracetamol_train.xyz', train_db)
write('./dataset/paracetamol_test.xyz', test_db)