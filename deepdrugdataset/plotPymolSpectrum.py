#!/usr/bin/env python
# coding: utf-8
"""
for a given pdb fragment, visualise it with pymol.
"""

import json
import subprocess
import os
import argparse

#
# with open("goodExamples.json", mode='r') as inputFile:
#     samples = json.load(inputFile)
# # sort samples by fragment size
#
# samples = sorted(samples, key=lambda k: int(k['size']), reverse=True)


def makePNG(pdbRef):
    """Take a fragment, create a PNG with Pymol."""
    # run pymol with the input string
    vizString = r"""load {0}

remove solvent


hide all
show sticks
bg_color white
spectrum b, blue_red

set ray_shadows, 0
set surface_mode, 1
set cartoon_side_chain_helper, on
set cartoon_smooth_loops = 0
set cartoon_fancy_helices = 1
set cartoon_fancy_sheets = 1
set sphere_scale, 0.3
set opaque_background=0
set antialias = on
set line_smooth = 1
set depth_cue = 1
set specular = 1
set surface_quality = 1
set stick_quality = 15
set sphere_quality = 2
set cartoon_sampling = 14
set ribbon_sampling = 10
set ray_trace_fog = 0.8
set light = (-0.2,0,-1)
set ray_trace_mode = 1
""".format(pdbRef)

    with open("temp.pml", mode='w') as pmlFile:
        pmlFile.write(vizString)
    subprocess.run("pymol -q temp.pml", shell=True)



parser = argparse.ArgumentParser()
parser.add_argument("filename", help="the PDB file to be parsed")
args = parser.parse_args()

makePNG(args.filename)
