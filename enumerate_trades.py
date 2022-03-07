#!/usr/bin/env python3

import argparse
import json
import pathlib

from trade_value import *

# TODO: read from game files
TRADEABLE_STANCES = {
    'neutral',
    'wary',
    'receptive',
    'cordial',
    'friendly',
    'protective',
    'loyal',
    'patronizing',
    'custodial',
    'enigmatic',
}

parser = argparse.ArgumentParser()
parser.add_argument("save_file_json", type=pathlib.Path, help="Save file, but converted to JSON")
parser.add_argument("proposer", type=str)
parser.add_argument("trade_willingness", type=float) # TODO: read from save file instead
parser.add_argument("resource", type=Resource, choices=[c for c in Resource])
args = parser.parse_args()

with open(args.save_file_json) as f:
    gamestate = json.load(f)

countries = {
    k: v
    for k, v in gamestate['country'][0].items()
    if type(v[0]) == dict
}
countries_by_name = {
    c[0]['name'][0]: c[0]
    for c in countries.values()
}
ids_by_name = {
    v[0]['name'][0]: k
    for k, v in countries.items()
}
proposer = countries_by_name[args.proposer]
proposer_id = ids_by_name[args.proposer]

friendly_enough_to_trade = []
for name, country in countries_by_name.items():
    if name == args.proposer:
        continue
    if 'attitude' not in country['ai'][0]:
        # print(f"{name} has no attitude?")
        continue
    attitude_list = country['ai'][0]['attitude'][0]
    attitude_towards_me = [c for c in attitude_list if c['country'][0] == proposer_id]
    if len(attitude_towards_me) == 0:
        # print(f"{name} has no attitude towards {args.proposer}")
        continue
    assert len(attitude_towards_me) == 1
    attitude_towards_me = attitude_towards_me[0]
    if attitude_towards_me['attitude'][0] in TRADEABLE_STANCES:
        friendly_enough_to_trade.append(name)
friendly_enough_to_trade.sort()

def income(country, resource: Resource):
    return sum(
        float(d[0][resource.value][0])
        for d in country['budget'][0]['current_month'][0]['income'][0].values()
        if d[0] is not None and resource.value in d[0])


def resources_for(country):
    return {
        Resource(k): float(v[0])
        for k, v in country['modules'][0]['standard_economy_module'][0]['resources'][0].items()
        if k in Resource.__members__
    }

proposer_resources = resources_for(proposer)

def generate_minimal_steps(proposer, recipient, resource: Resource, trade_willingness: float):
    proposer_resources = resources_for(proposer)
    recipient_resources = resources_for(recipient)
    last_val = 0
    for offeredAmount in range(int(proposer_resources[resource])+1):
        val = trade_value_for_recipient(
            resource=resource,
            offeredAmount=offeredAmount,
            senderIncome=income(proposer, resource),
            recipientIncome=income(recipient, resource),
            recipientTradeWillingness=trade_willingness,
            recipientCurrentStockpile=recipient_resources[resource],
            recipientResourceCap=25000, # TODO: read from save file somehow
        )
        if last_val != val:
            yield (offeredAmount, val)
        last_val = val

def find_energy_price_for(recipient, trade_value: int):
    for energyBack in range(1000, 0, -1):
        energy_val = trade_value_for_recipient(
            resource=Resource.energy,
            offeredAmount=energyBack,
            senderIncome=income(recipient, Resource.energy),
            recipientIncome=income(proposer, Resource.energy),
            recipientTradeWillingness=1,
            recipientCurrentStockpile=proposer_resources[Resource.energy],
            recipientResourceCap=25000, # TODO: read from save file somehow
        )
        if trade_value - energy_val == 1:
            return energyBack


for partner_name in friendly_enough_to_trade:
    print(partner_name, ids_by_name[partner_name])
    partner = countries_by_name[partner_name]
    for offeredAmount, val in generate_minimal_steps(proposer, partner, args.resource, args.trade_willingness):
        print(offeredAmount, find_energy_price_for(partner, val))
