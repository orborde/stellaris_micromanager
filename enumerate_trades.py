#!/usr/bin/env python3

import argparse
import json
import pathlib

from trade_value import *

parser = argparse.ArgumentParser()
parser.add_argument("save_file_json", type=pathlib.Path, help="Save file, but converted to JSON")
parser.add_argument("proposer_id", type=int)
parser.add_argument("recipient_id", type=int)
parser.add_argument("trade_willingness", type=float) # TODO: read from save file instead
parser.add_argument("resource", type=Resource, choices=[c for c in Resource])
args = parser.parse_args()

with open(args.save_file_json) as f:
    gamestate = json.load(f)

countries = gamestate['country'][0]
proposer = countries[str(args.proposer_id)][0]
recipient = countries[str(args.recipient_id)][0]

def income(country, resource: Resource):
    return sum(
        float(d[0][resource.value][0])
        for d in country['budget'][0]['current_month'][0]['income'][0].values()
        if d[0] is not None and resource.value in d[0])


recipient_resources = {
    Resource(k): float(v[0])
    for k, v in recipient['modules'][0]['standard_economy_module'][0]['resources'][0].items()
    if k in Resource.__members__
}

last_val = None
for offeredAmount in range(300):
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
        print(offeredAmount, val)
    last_val = val