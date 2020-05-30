#!/usr/bin/env python3

import argparse
import os
import os.path

parser=argparse.ArgumentParser()
parser.add_argument("dir")
args = parser.parse_args()

autosaves = [f for f in os.listdir(args.dir) if f.startswith('autosave_')]
autosaves.sort()
print(os.path.join(args.dir, autosaves[-1]))
