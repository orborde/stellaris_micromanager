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
    "Unified Consciousness",
    "CUDDLE PUDDLE",
}

for c in gamestate['country'][0].values():
    if c == ['none']:
        continue

    c=c[0]
    name=c['name'][0]
    if name not in TARGET_COUNTRIES:
        continue

    timed_modifiers = c['timed_modifier']
    ci_mod = list(filter(lambda m: m['modifier'][0] == 'curator_insight', timed_modifiers))
    assert len(ci_mod) in [0,1]
    if len(ci_mod) == 0:
        print(name, 'lacks Curator Insight! :(')
    else:
        ci_mod = ci_mod[0]
        print(name, float(ci_mod['days'][0]), 'days remaining')
