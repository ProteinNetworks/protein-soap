"""
Reads in the deepdrug3d datasets, scrubs the element names (which are Ca, Cb, Oa-g etc). If the 
residues flag is given, only save the Ca.
"""

import quippy
import ase
import json
from ase.atoms import Atoms as AseAtoms
import warnings
import argparse
import os
import glob
warnings.filterwarnings('error', "Discarding atom when reading PDB file")

# Because of the daft labelling, I need to strip all the element symbols and relabel them.
def relabelElementNames(filePath, only_keep_alphas=False):
    with open(proteinLabel) as flines:
        data = [line.strip() for line in flines]
    new_data = []
    for line in data:
        if not line.startswith("ATOM"):
            # Do nothing
            new_data.append(line)
            continue
        atom_name = line[12:16]
        if only_keep_alphas and atom_name.strip() == "CA":
            # convert the CA to a C and push to the new file
            new_line = line[:12] + line[12:16].replace("CA", "C ") + line[16:]
            new_data.append(new_line)
        elif not only_keep_alphas:
            # replace C* with C, S* with S, N* with N, O* with O
            if not line[13].strip():
                raise IndexError("the spacing is off!")
            if line[13] not in ["C", "S", "N", "O", "H"]:
                print "Warning", line[12:16]
            new_line = line[:14] + "  " + line[16:]
            new_data.append(new_line)
    newLabel = proteinLabel[:-4] + "_converted" + proteinLabel[-4:]
    with open(newLabel, "w") as flines:
        flines.write("\n".join(new_data))
    return newLabel

if __name__ == "__main__":
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
        newLabel = relabelElementNames(proteinLabel, args.residues)
        try:
            temp = quippy.Atoms(ase.io.read(newLabel, format='proteindatabank')) # done like this to catch warning
            proteinHolder.append(temp)
            labels.append([hemeLabel, "heme"])
        except Warning:
            print("!!")
            continue
    for nucleoLabel in nucleoProteins:
        proteinLabel = nucleoInputDir + "/" + nucleoLabel
        newLabel = relabelElementNames(proteinLabel, args.residues)
        try:
            temp = quippy.Atoms(ase.io.read(newLabel, format='proteindatabank')) # done like this to catch warning
            proteinHolder.append(temp)
            labels.append([nucleoLabel, "nucleo"])
        except Warning:
            print("!!")
            continue

    with open("test_labels.txt", "w") as flines:
        flines.write("\n".join(" ".join(x) for x in labels))

    testFamily = quippy.AtomsList(proteinHolder)
    print(len(testFamily), "proteins converted to xyz")
    print(len(labels), "labels listed")
    testFamily.write("test_proteinstructures.xyz")

    xyzFileName= "test_proteinstructures.xyz"
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
    with open("test_proteinstructures_tagged.xyz", "w") as flines:
        flines.write("\n".join(newdata))


