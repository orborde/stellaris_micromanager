#!/usr/bin/env python3

import argparse
import os
import os.path
import pathlib
import shutil
import subprocess
import tempfile
import time

parser=argparse.ArgumentParser()
parser.add_argument("dir", type=str, help='directory where new autosave files will appear')
parser.add_argument("cmd", type=str, help='command to run')
parser.add_argument('--interval', type=int, default=1, help='poll interval (seconds)')
parser.add_argument(
    '--dump_location', default='/tmp/broken.sav',
    help='when the subcommand fails, put the offending savegame at this path')
parser.add_argument('--json_archive', type=pathlib.Path, default="",
    help="If set, put a copy of generated JSON file here")
args = parser.parse_args()

interval=float(args.interval)

def execute(path):
    start = time.time()
    jsondata = subprocess.check_output(['./sav2json', '-infile', path])
    parsed = time.time()
    if args.json_archive != "":
        copy_path = args.json_archive / (os.path.basename(path) + ".json")
        with open(copy_path, 'wb') as f:
            f.write(jsondata)
            print('wrote a copy to', copy_path)
    with tempfile.NamedTemporaryFile() as tf:
        tf.write(jsondata)
        tf.flush()

        subprocess.check_call([args.cmd, tf.name])
    analyzed = time.time()
    print(f'...analyzed! (parsed: {parsed-start:.2f}s, analyzed: {analyzed-parsed:.2f}s)')


last_processed = None
while True:
    autosaves = [f for f in os.listdir(args.dir) if f.startswith('autosave_') and f.endswith(".sav")]
    autosaves.sort()
    autosave = autosaves[-1]

    if last_processed is None or last_processed < autosave:
        fullpath = os.path.join(args.dir, autosaves[-1])
        print('found new autosave', fullpath)
        try:
            execute(fullpath)
        except Exception as e:
            print('dumping to', args.dump_location)
            shutil.copyfile(fullpath, args.dump_location)
            raise e
        last_processed = autosave

    time.sleep(interval)
