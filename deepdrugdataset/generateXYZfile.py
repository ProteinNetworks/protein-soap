import quippy
import ase
import json
from ase.atoms import Atoms as AseAtoms
import warnings
import argparse
import os
import glob
warnings.filterwarnings('error', "Discarding atom when reading PDB file")


parser = argparse.ArgumentParser()
parser.add_argument("hemedirectory", help="the heme directory to use when generating the XYZ file")
parser.add_argument("nucleotidedirectory", help="the nucleotide directory to use when generating the XYZ file")
parser.add_argument("--residues", help="whether or not to use the alpha-carbons only", action="store_true")
args = parser.parse_args()

hemeInputDir = args.hemedirectory
hemeProteins = os.listdir(hemeInputDir)
print(len(hemeProteins), "proteins in heme directory")

nucleoInputDir = args.nucleotidedirectory
nucleoProteins = os.listdir(nucleoInputDir)
print(nucleoInputDir)
print(len(nucleoProteins), "proteins in nucleotide directory")

proteinHolder = []
labels = []
for hemeLabel in hemeProteins:
    proteinLabel = hemeInputDir + "/" + hemeLabel
    try:
        temp = quippy.Atoms(ase.io.read(proteinLabel, format='proteindatabank')) # done like this to catch warning
        proteinHolder.append(temp)
        labels.append([hemeLabel, "heme"])
    except Warning:
        print("!!")
        continue
for nucleoLabel in nucleoProteins:
    proteinLabel = nucleoInputDir + "/" + nucleoLabel
    try:
        temp = quippy.Atoms(ase.io.read(proteinLabel, format='proteindatabank')) # done like this to catch warning
        proteinHolder.append(temp)
        labels.append([nucleoLabel, "nucleo"])
    except Warning:
        print("!!")
        continue

with open("intermediates/labels.txt", "w") as flines:
    flines.write("\n".join(" ".join(x) for x in labels))

testFamily = quippy.AtomsList(proteinHolder)
print(len(testFamily), "proteins converted to xyz")
print(len(labels), "labels listed")
testFamily.write("intermediates/proteinstructures.xyz")

xyzFileName= "intermediates/proteinstructures.xyz"
with open(xyzFileName) as flines:
    data = [line.strip() for line in flines]
newdata = []
counter = 0 
for line in data:
    if line.startswith("cutoff"):
        label = labels[counter][0][:-4] + "_" + labels[counter][1]
        line += " tag=\"{}\" ".format(label)
        counter += 1
    newdata.append(line)
assert len(newdata) == len(data)
assert len(labels) == counter
with open("intermediates/proteinstructures_tagged.xyz", "w") as flines:
    flines.write("\n".join(newdata))


