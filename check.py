#!/usr/bin/env python3

import argparse
import collections
import json
import logging
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument("infile")
parser.add_argument(
    '--show-modifier-time-remaining', default=False, type=bool,
    help="Show remaining time on timed modifiers")
args = parser.parse_args()

with open(args.infile) as i:
    gamestate = json.load(i)


# TARGET_COUNTRIES={
#     "Unified Consciousness",
#     "CUDDLE PUDDLE",
# }


TARGET_COUNTRIES={
    'Interstellar Orc Horde',
    'YOLO',
}

def check_timed_modifier(country, modifier: str):
    if 'timed_modifier' not in country:
        return

    name = country['name']
    timed_modifiers = country['timed_modifier']
    ci_mod = list(filter(lambda m: m['modifier'][0] == modifier, timed_modifiers))
    assert len(ci_mod) in [0,1]
    if len(ci_mod) == 0:
        print(name, 'lacks', modifier, ':(')
    elif args.show_modifier_time_remaining:
        ci_mod = ci_mod[0]
        print(name, float(ci_mod['days'][0]), 'days remaining on', modifier)

def check_unexploited_deposits(country_name, country_id, galactic_objects, planets):
    country_systems = [obj[0] for obj in galactic_objects.values() if obj[0]['starbase'][0]==country_id]
    country_planet_ids = sum((obj['planet'] for obj in country_systems), [])
    country_planets = [planets['planet'][0][pid] for pid in country_planet_ids]

    for planet in country_planets:
        planet = planet[0]
        if 'deposits' not in planet:
            continue

        deposits = planet['deposits'][0]
        if len(deposits) > 0 and 'shipclass_orbital_station' not in planet:
            print(country_name, ':', planet['name'][0], 'unexploited deposits', deposits)


countries = gamestate['country'][0]

techs_countries = collections.defaultdict(set)

for cid, c in countries.items():
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
        for item in tech[queue][0]:
            if 'technology' in item:
                researching = item['technology'][0]
                techs_countries[researching].add(name)

    check_timed_modifier(c, 'curator_insight')
    check_timed_modifier(c, 'enclave_artist_patron')
    check_timed_modifier(c, 'enclave_artist_festival')
    check_unexploited_deposits(
        name, cid,
        gamestate['galactic_object'][0],
        gamestate['planets'][0])

for tech in techs_countries:
    if len(techs_countries[tech]) > 1:
        print(tech,'being research by',techs_countries[tech])
