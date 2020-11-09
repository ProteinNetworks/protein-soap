# Get all ligands

import subprocess

with open("labels.txt") as flines:
    labels = [line.strip() for line in flines]

for label in labels:
    print(label)
    pdb_ref = label[:4]
    chain_ref = label[4]
    subprocess.call(["wget","http://www.rcsb.org/pdb/files/{}.pdb".format(pdb_ref), "-q"])
    ligands = set()
    with open("{}.pdb".format(pdb_ref)) as flines:
        pdb_data = flines.readlines()
        ligand_data = []
        for line in pdb_data:
            if line.startswith("HETATM") and line[21] == chain_ref:
                ligands.add(line[17:20])
    print(ligands)
