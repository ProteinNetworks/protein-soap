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

def addLigand(filename):
    """
    Given a filename, get the associated ligand and add it to the pdb file.
    """
    basename = os.path.basename(filename)
    pdbAndChain, ligandType, _ = basename[:13].split("_")
    assert len(pdbAndChain) == 5
    pdbRef = pdbAndChain[:4]
    chainRef = pdbAndChain[4]
    if ligandType == "heme":
        ligandID = "HEM"
    elif ligandType == "nucleo":
        ligandID = "ATP"
    else:
        raise IOError
    with open(filename, "r") as flines:
        original_data = [line.strip() for line in flines]
    beginnings = set([x[:6] for x in original_data])
    print(beginnings)
    if "HETATM" in beginnings:
        # then we have already added the ligand data
        return
    else:
        subprocess.run(f"wget http://www.rcsb.org/pdb/files/{pdbRef}.pdb", shell=True)

        with open(f"{pdbRef}.pdb") as flines:
            pdbData = flines.readlines()
        
        os.remove(f"{pdbRef}.pdb")
        ligand_data = []
        for line in pdbData:
            # if line.startswith("HETATM") and line[17:20] == ligandID and line[21] == chainRef:
            if line.startswith("HETATM") and line[21] == chainRef:
                ligand_data.append(line.strip())
        
        # Now we have the ligand atom positions. Append these to our original file file
        if original_data[-1].startswith("ENDMDL"):
            ligand_data = original_data[:-1] + ligand_data + ["ENDMDL"]
            print(ligand_data)
        else:
            ligand_data = original_data + ligand_data

        with open(filename, "w") as flines:
            flines.write("\n".join(ligand_data))


def makePNG(pdbRef):
    """Take a fragment, create a PNG with Pymol."""
    # run pymol with the input string
    vizString = r"""load {0}

remove solvent


hide all
show sticks
bg_color white
spectrum b, blue_red, minimum=0.95, maximum=1.0

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
colour green, hetatm
""".format(pdbRef)

    with open("temp.pml", mode='w') as pmlFile:
        pmlFile.write(vizString)
    addLigand(pdbRef)
    subprocess.run("pymol -q temp.pml", shell=True)



parser = argparse.ArgumentParser()
parser.add_argument("filename", help="the PDB file to be parsed")
args = parser.parse_args()

makePNG(args.filename)
