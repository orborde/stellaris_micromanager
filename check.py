#!/usr/bin/env python3

import argparse
import collections
import json

parser = argparse.ArgumentParser()
parser.add_argument("infile")
parser.add_argument("target_countries", nargs='+', type=str)
parser.add_argument(
    '--show-modifier-time-remaining', default=False, type=bool,
    help="Show remaining time on timed modifiers")
args = parser.parse_args()

with open(args.infile) as i:
    gamestate = json.load(i)

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

def check_unexploited_deposits(country_name, country_id, galactic_objects, planets, deposit):
    DEPOSIT_TYPES = {'d_' + x for x in [
        'alloys',
        'dark_matter_deposit',
        'energy',
        'engineering',
        'exotic_gases',
        'minerals',
        'physics',
        'rare_crystals',
        'society',
        'volatile_motes',
        'zro_deposit',
    ]}

    country_systems = [obj[0] for obj in galactic_objects.values() if obj[0]['starbase'][0]==country_id]
    for system in country_systems:
        planet_ids = system['planet']
        planets = [planets['planet'][0][pid] for pid in planet_ids]

        for planet in planets:
            planet = planet[0]
            if 'deposits' not in planet:
                continue

            # There's a station, so any deposits are exploited.
            if 'shipclass_orbital_station' in planet:
                continue

            deposits = planet['deposits'][0]
            deposit_types = (deposit[d][0]['type'][0] for d in deposits)
            checked_deposits = [d for d in deposit_types if d.rsplit('_', 1)[0] in DEPOSIT_TYPES]
            if len(checked_deposits) > 0:
                print(country_name, ':', system['name'][0], '/', planet['name'][0],
                    'unexploited deposits:', checked_deposits)


countries = gamestate['country'][0]

techs_countries = collections.defaultdict(set)

for cid, c in countries.items():
    if c == ['none']:
        continue

    c=c[0]
    name=c['name'][0]
    if name not in args.target_countries:
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
        gamestate['planets'][0],
        gamestate['deposit'][0])

for tech in techs_countries:
    if len(techs_countries[tech]) > 1:
        print(tech,'being research by',techs_countries[tech])
