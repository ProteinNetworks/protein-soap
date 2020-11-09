"""
Check that the sampled XYZ file does contain 100 HEM binders, and 100 ATP binders
"""

import argparse
import quippy
import numpy as np


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pathToXYZFile", help="the path to the xyz file")
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
