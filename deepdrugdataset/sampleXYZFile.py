"""
Given an xyz file containing heme and nucleotide tagged entries,
sample the given number of each and make a smaller xyz file.

"""

import argparse
import quippy
import numpy as np


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pathToXYZFile", help="the path to the xyz file")
    parser.add_argument("--sampleSize", type=int, help="the number of heme and nucleotide samples to draw")
    args = parser.parse_args()

    input_file = quippy.AtomsReader(args.pathToXYZFile, format="xyz")
    hemes = []
    nucleos = []
    for protein in input_file:
        label = protein.params["tag"]
        if label[6:] == "heme":
            hemes.append(label)
        else:
            nucleos.append(label)


    print(len(hemes))
    print(len(nucleos))

    print repr(hemes)
    print repr(nucleos)
#    #sample 100 from the numbers 0-596, and 100 from the numbers 596-2149
    # 402 hemes
    # 260 nucleos
    num_heme = 402
    num_nucleo = 260
    heme_samples = np.random.choice(range(num_heme), size=args.sampleSize)
    nucleo_samples = np.random.choice(range(num_heme, num_heme+num_nucleo), size=args.sampleSize)
    samples = list(heme_samples)+list(nucleo_samples)
    out = quippy.io.AtomsWriter("intermediates/samples_filtered.xyz")
    for i in samples:
       out.write(input_file[i])
    out.close()
