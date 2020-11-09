#!/usr/bin/env python3
"""
Inputs: The location of the PDB file and the .tree file.
Then:
    - Pull the tree file into a numpy array.
    - Generate a PyMol script for each column of the array
    - Run a PyMoL script that loads each level separately.
"""

import argparse
import numpy as np
import os
from pythonModules import treeFileToNumpyArray

parser = argparse.ArgumentParser()
parser.add_argument("pdbfilename", help="the PDB file to be parsed")
parser.add_argument(
    "treefilename", help="the Infomap output file to be parsed")
parser.add_argument("--output", "-o", help="the name of the output .pse file")
args = parser.parse_args()

inputArray = treeFileToNumpyArray(args.treefilename)
# drop the node index
inputArray = inputArray[:, :-1]
pdbRef = os.path.splitext(os.path.basename(args.pdbfilename))[0]
output = args.output if args.output else "{}.pse".format(pdbRef)
"""
Generate the sequence of b-factor alterations for each level.
Each column of the input Array alters a Pymol Object of the form
$PDBREF_$INDEX where the pdbref is the 4-character identifier, and index the
column number (starting from zeros)
"""
pymolCommands = []
for i, col in enumerate(inputArray.T):
    numberOfCommunities = len(set(col))

    pymolCommand = "\n".join([
        "alter {0}_{1} and (index {2} ), b={3}".format(
            pdbRef, i,
            " or index ".join(str(x + 1) for x in np.where(col == com)[0]),
            com / numberOfCommunities) for com in set(col)
    ])
    pymolCommands.append(pymolCommand)
"""
Amalgamate the pymol commands so as to load a pdb file for each level of hierarchy,
then run the bfactor alterations.
"""

pymolScript = "\n".join([
    "load {0}, {1}_{2}".format(args.pdbfilename, pdbRef, i)
    for i in range(len(pymolCommands))
])
pymolScript += "\n"
pymolScript += "\n".join(pymolCommands)
pymolScript += """

#formatting
bg_color white
hide all
#show sticks
show cartoon
spectrum b, rainbow,  minimum=0, maximum=1
set opaque_background=0
set antialias = on
set line_smooth = 1
set depth_cue = 1
set specular = 1
set surface_quality = 1
set stick_quality = 15
set sphere_quality = 2
set ray_trace_fog = 0.8
set light = (-0.2,0,-1)

set ray_shadows, 0
set surface_mode, 1
set cartoon_side_chain_helper,on
rebuild
save {}
""".format(output)

print(pymolScript)  # For now, just pipe this to pymol -pcq
