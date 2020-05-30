#!/usr/bin/env python3

import argparse
import collections
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

techs_countries = collections.defaultdict(set)

for c in gamestate['country'][0].values():
    if c == ['none']:
        continue

    c=c[0]
    name=c['name'][0]
    if name not in TARGET_COUNTRIES:
        continue

    tech = c['tech_status'][0]
    for t in ['physics', 'society', 'engineering']:
        queue=t+'_queue'
        if queue not in tech:
            continue
        for item in tech[queue][0][0]:
            if 'technology' in item:
                researching = item['technology'][0]
                techs_countries[researching].add(name)

    if 'timed_modifier' not in c:
        continue

    timed_modifiers = c['timed_modifier']
    ci_mod = list(filter(lambda m: m['modifier'][0] == 'curator_insight', timed_modifiers))
    assert len(ci_mod) in [0,1]
    if len(ci_mod) == 0:
        print(name, 'lacks Curator Insight! :(')
    else:
        ci_mod = ci_mod[0]
        print(name, float(ci_mod['days'][0]), 'days remaining')

for tech in techs_countries:
    if len(techs_countries[tech]) > 1:
        print(tech,'being research by',techs_countries[tech])