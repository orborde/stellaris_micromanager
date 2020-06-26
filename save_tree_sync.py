#! /usr/bin/env python3

import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("src", type=str)
parser.add_argument("dst", type=str)
args = parser.parse_args()

subprocess.check_call(
    [
        'rsync',
        '-av',
        '--prune-empty-dirs',
        '--include=*/',
        '--include=*.sav',
        '--exclude=*',
        args.src, args.dst,
    ])
