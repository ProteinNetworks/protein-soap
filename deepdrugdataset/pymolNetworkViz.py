#!/usr/bin/env python
# coding: utf-8
"""
for a given edgelist, read in the edges., pull and visualise the atoms,
then manually bond pairs of atoms according to the edgelist.
"""

import subprocess
import os
import argparse
from pythonModules import treeFileToNumpyArray


def makePNG(fragmentID, pdbFilename):
    """Take an edgelist, create a PNG with Pymol."""
    # load the input molecule
    with open("temp.pml", mode='w') as pmlFile:
        pmlFile.write("load {0}\n".format(pdbFilename))
        pmlFile.write(r"""remove solvent
hide all
show spheres
set sphere_scale, 0.25, (all)
set stick_radius=0.1
unbond (all), (all)
show sticks
set antialias = on
set depth_cue = 1
set specular = 1
set surface_quality = 1
set stick_quality = 15
set sphere_quality = 2
alter (all), b=0.0
""")

        # add the bonding information
        with open(fragmentID) as flines:
            for line in flines:
                ID1 = line.split()[0]
                ID2 = line.split()[1]
                pmlFile.write('cmd.bond("id {0}", "( id {1})")\n'.format(ID1, ID2))
        
        # add the community information, and colour
        commArray = treeFileToNumpyArray("{}.tree".format(fragmentID[:-4]))[:,args.level]
        numComs = len(set(commArray))
        for index, val in enumerate(commArray):
            pmlFile.write('cmd.alter("id {0}","b={1}")\n'.format(index+1, val/numComs))
        pmlFile.write('spectrum b, yrmbcg, minimum=0, maximum=1\n')
        pmlFile.write('save {0}.pse'.format(pdbFilename[:-4]))

    subprocess.run("pymol -q temp.pml", shell=True)



parser = argparse.ArgumentParser()
parser.add_argument("filename", help="the edgelist to be parsed")
parser.add_argument("pdbfilename", help="the pdb to be parsed")

parser.add_argument("--level", help="the infomap level to view", type=int, default=0)
args = parser.parse_args()

makePNG(args.filename, args.pdbfilename)
