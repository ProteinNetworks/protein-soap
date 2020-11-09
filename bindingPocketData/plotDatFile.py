#!/usr/bin/env python
# coding: utf-8
"""
for a given pdb fragment, visualise it with pymol.
"""

import json
import subprocess
import os
import argparse
import matplotlib.pyplot as plt


parser = argparse.ArgumentParser()
parser.add_argument("filename", help="the PDB file to be parsed")
args = parser.parse_args()

with open(args.filename) as flines:
    data = [line.strip().split() for line in flines]

print(data[0])

data = data[1:]
plt.scatter([x[4] for x in data], [x[2] for x in data], c="blue", label="heme")
plt.scatter([x[4] for x in data], [x[3] for x in data], c="orange", label="nucleo")
plt.legend()
plt.savefig("temp.png")
plt.show()

