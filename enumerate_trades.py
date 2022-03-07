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
parser.add_argument("--book_size", type=int, default=3)
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

def generate_minimal_steps(sender, recipient, resource: Resource, trade_willingness: float):
    sender_resources = resources_for(sender)
    recipient_resources = resources_for(recipient)
    last_val = 0
    for offeredAmount in range(int(sender_resources[resource])+1):
        val = trade_value_for_recipient(
            resource=resource,
            offeredAmount=offeredAmount,
            senderIncome=income(sender, resource),
            recipientIncome=income(recipient, resource),
            recipientTradeWillingness=trade_willingness,
            recipientCurrentStockpile=recipient_resources[resource],
            recipientResourceCap=25000, # TODO: read from save file somehow
        )
        if last_val != val:
            yield (offeredAmount, val)
        last_val = val

def find_maximal_for(partner, trade_value: int, resource: Resource):
    partner_resources = resources_for(partner)
    partner_stockpile = partner_resources[resource]
    for resource_back in range(int(partner_stockpile), 0, -1):
        val = trade_value_for_recipient(
            resource=resource,
            offeredAmount=resource_back,
            senderIncome=income(partner, resource),
            recipientIncome=income(proposer, resource),
            recipientTradeWillingness=1,
            recipientCurrentStockpile=proposer_resources[resource],
            recipientResourceCap=25000, # TODO: read from save file somehow
        )
        if trade_value - val == 1:
            return resource_back


def generate_bids(partner, resource: Resource, trade_willingness: float):
    for offeredAmount, val in generate_minimal_steps(proposer, partner, resource, trade_willingness):
        price = find_maximal_for(partner, val, Resource.energy)
        yield (offeredAmount, price)

def generate_asks(partner, resource: Resource, trade_willingness: float):
    for energy_amt, val in generate_minimal_steps(partner, proposer, Resource.energy, trade_willingness):
        volume = find_maximal_for(partner, val, resource)
        yield (volume, energy_amt)


for partner_name in friendly_enough_to_trade:
    print(partner_name, ids_by_name[partner_name])
    partner = countries_by_name[partner_name]
    bids = list(generate_bids(partner, args.resource, args.trade_willingness))
    asks = list(generate_asks(partner, args.resource, args.trade_willingness))

    for volume,price in bids[:args.book_size]:
        print(f"  BID {volume} @ {price}")
    for volume,price in asks[:args.book_size]:
        print(f"  ASK {volume} @ {price}")
    print()