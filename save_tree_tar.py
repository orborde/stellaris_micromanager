#! /usr/bin/env python3

import argparse
import io
import logging
import os
import tarfile
import sys
import zipfile

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

parser = argparse.ArgumentParser()
parser.add_argument("save_directory", type=str)
args = parser.parse_args()

saves = sorted(os.listdir(args.save_directory))

with os.fdopen(sys.stdout.fileno(), "wb", closefd=False) as stdout:
    with tarfile.open(mode='w|', fileobj=stdout) as tar:
        for n, f in enumerate(saves):
            path = os.path.join(args.save_directory, f)
            logging.info('processing %d/%d: %s', (n+1), len(saves), path)

            ident, suff = os.path.splitext(f)
            assert suff == '.sav', suff

            with zipfile.ZipFile(path, 'r') as zf:
                for cmpt in zf.filelist:
                    data = zf.read(cmpt)

                    dest = os.path.join(ident, cmpt.filename)
                    tarinfo = tarfile.TarInfo(dest)
                    tarinfo.size = len(data)
                    bytebuf = io.BytesIO(data)
                    tar.addfile(tarinfo=tarinfo, fileobj=bytebuf)

                    logging.info("%s %s -> %s: %d bytes",
                        path, cmpt.filename, dest,
                        len(data))

