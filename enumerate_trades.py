#!/usr/bin/env python3

import argparse
import json
import pathlib

from trade_value import *

parser = argparse.ArgumentParser()
parser.add_argument("save_file_json", type=pathlib.Path, help="Save file, but converted to JSON")
parser.add_argument("proposer", type=str)
parser.add_argument("recipient", type=str)
parser.add_argument("trade_willingness", type=float) # TODO: read from save file instead
parser.add_argument("resource", type=Resource, choices=[c for c in Resource])
args = parser.parse_args()

with open(args.save_file_json) as f:
    gamestate = json.load(f)

countries = gamestate['country'][0]
countries_by_name = {
    c[0]['name'][0]: c[0]
    for c in countries.values()
    if type(c[0]) is dict # seriously wtf
}
proposer = countries_by_name[args.proposer]
recipient = countries_by_name[args.recipient]

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

recipient_resources = resources_for(recipient)
proposer_resources = resources_for(proposer)

def generate_steps(proposer, recipient):
    last_val = 0
    for offeredAmount in range(100):
        val = trade_value_for_recipient(
            resource=args.resource,
            offeredAmount=offeredAmount,
            senderIncome=income(proposer, args.resource),
            recipientIncome=income(recipient, args.resource),
            recipientTradeWillingness=args.trade_willingness,
            recipientCurrentStockpile=recipient_resources[args.resource],
            recipientResourceCap=25000, # TODO: read from save file somehow
        )
        if last_val != val:
            yield (offeredAmount, val)
        last_val = val

def find_energy_price_for(trade_value: int):
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


for offeredAmount, val in generate_steps(proposer, recipient, args.resource, args.trade_willingness):
    print(offeredAmount, val, find_energy_price_for(val))
