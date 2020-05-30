#!/usr/bin/env python3

import argparse
import json
import logging
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument("infile")
args = parser.parse_args()

with open(args.infile) as i:
    gamestate = json.load(i)


TARGET_COUNTRIES={
    '"Unified Consciousness"',
    '"CUDDLE PUDDLE"',
}

for c in gamestate['country'][0].values():
    if c == ['none']:
        continue

    c=c[0]
    name=c['name'][0]
    if name not in TARGET_COUNTRIES:
        continue

    timed_modifiers = c['timed_modifier']
    print(name, any(modifier['modifier'][0] == '"curator_insight"' for modifier in timed_modifiers))
