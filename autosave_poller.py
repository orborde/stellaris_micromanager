#!/usr/bin/env python3

import argparse
import os
import os.path
import subprocess
import tempfile
import time

parser=argparse.ArgumentParser()
parser.add_argument("dir")
parser.add_argument('interval')
args = parser.parse_args()

interval=float(args.interval)

def execute(path):
    jsondata = subprocess.check_output(['./sav2json', path])
    with tempfile.NamedTemporaryFile() as tf:
        tf.write(jsondata)
        tf.flush()
        tf.close()

        subprocess.check_call(['./check.py', tf.name])


last_processed = None
while True:
    autosaves = [f for f in os.listdir(args.dir) if f.startswith('autosave_')]
    autosaves.sort()
    autosave = autosaves[-1]

    if last_processed is None or last_processed < autosave:
        fullpath = os.path.join(args.dir, autosaves[-1])
        print('found new autosave', fullpath)
        execute(fullpath)

    time.sleep(interval)
