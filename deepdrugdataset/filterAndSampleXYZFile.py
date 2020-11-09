"""
Given an xyz file containing heme and nucleotide tagged entries,
sample the given number of each and make a smaller xyz file.

The first 596 frames are heme, the last 1553 are nucleo
"""

import argparse
import quippy
import numpy as np
import subprocess

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pathToXYZFile", help="the path to the xyz file")
    parser.add_argument("pathToOutputXYZFile", help="the path to the output XYZ xyz file")
    parser.add_argument("--sampleSize", type=int, help="the number of heme and nucleotide samples to draw")
    args = parser.parse_args()

    input_file = quippy.AtomsReader(args.pathToXYZFile, format="xyz")
    output_file = quippy.AtomsWriter(args.pathToOutputXYZFile, format="xyz")


    # Hemes are the indices from 0-595
    # Nucleos are from 596 to 2148

    # We want only HEM and ATP binders
    for i, protein in enumerate(input_file):
        label =  protein.params["tag"] 

        pdb_ref = label[:4]
        print(pdb_ref)
        chain_ref = label[4]
        protein_type = label[6:]
        subprocess.call(["wget","http://www.rcsb.org/pdb/files/{}.pdb".format(pdb_ref)])
        try:
            with open("{}.pdb".format(pdb_ref)) as flines:
                pdb_data = flines.readlines()
        except IOError:
            print("IO Error")
                
        if protein_type == "heme":
            ligand_id = ["HEM"]
        elif protein_type == "nucleo":
            ligand_id = ["ATP"]
        else:
            raise ValueError
        
        ligand_data = []
        for line in pdb_data:
            if line.startswith("HETATM"):
                if line[17:20].strip() in ligand_id and line[21] == chain_ref:
                    ligand_data.append(line.strip())

        if not ligand_data:
            print("No ligand found")
            continue
        else:
            print("ligand found")
            print(ligand_data)

        output_file.write(protein)

#    #sample 100 from the numbers 0-596, and 100 from the numbers 596-2149
#    num_heme = 596
#    num_nucleo = 1553
#    heme_samples = np.random.choice(range(num_heme), size=args.sampleSize)
#    nucleo_samples = np.random.choice(range(num_heme, num_heme+num_nucleo), size=args.sampleSize)
#    samples = list(heme_samples)+list(nucleo_samples)
#    out = quippy.io.AtomsWriter("samples.xyz")
#    for i in samples:
#        out.write(file[i])
#    out.close()
