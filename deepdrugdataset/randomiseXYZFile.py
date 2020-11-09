"""
Given an xyz file, randomise the entries.

Hopefully this rules out (or reveals) some bugs
"""

import argparse
import quippy
import numpy as np


path_to_xyz_file = "intermediates/samples2.xyz"
path_to_randomised_xyz_file = "intermediates/samples2_randomised.xyz"
input_file = quippy.AtomsReader(path_to_xyz_file, format="xyz")


size_of_input = len(input_file)
samples = list(range(size_of_input))
np.random.shuffle(samples)

out = quippy.io.AtomsWriter(path_to_randomised_xyz_file)
for i in samples:
    out.write(input_file[i])
out.close()
