#! /usr/bin/env python3

import collections
import itertools
import json
import math
from tqdm import tqdm
from typing import *

from trade_value import *
from enumerate_trades import *

def fulfill(
    desired_resource: Resource,
    desired_amount: int,
    original_currency: Resource,
    # TODO: offer should probably include currency type, and then you don't have to pass a dict here
    # Maps Currency -> Offers
    original_asks_by_currency: Dict[Resource, List[Offer]],
) -> List[Offer]:
    assert all(all(o.type == TradeType.ASK for o in offers) for offers in original_asks_by_currency.values())

    # TODO: this is banans
    currency_paths = collections.defaultdict(collections.defaultdict)
    for currency, offers in original_asks_by_currency.items():
        outbound = collections.defaultdict(list)
        for offer in offers:
            outbound[offer.resource].append(offer)
        for k in outbound:
            outbound[k] = sorted(outbound[k], key=lambda o: o.currency)
        currency_paths[currency] = outbound
    
    def helper(offer_path: List[Offer]) -> Optional[List[Offer]]:
        if len(offer_path) > 0:
            currency_resource = offer_path[-1].resource
            # Assume that only executable asks are in the offers list. This should be okay
            # since we should only be examining offers whose currencies have not yet been
            # used in the path.
            usable_currency_amount = offer_path[-1].amount
        else:
            currency_resource = original_currency
            usable_currency_amount = math.inf
        
        unbuyable_resources = set(o.resource for o in offer_path).union([original_currency])
        for resource_to_buy, offers in currency_paths[currency_resource].items():
            if resource_to_buy in unbuyable_resources:
                continue

            for offer in offers:
                assert offer.resource == resource_to_buy
            
                if offer.currency > usable_currency_amount:
                    continue

                new_path = offer_path + [offer]
                if resource_to_buy == desired_resource:
                    if offer.amount >= desired_amount:
                        return new_path
                else:
                    result = helper(new_path)
                    if result is not None:
                        return result
        
        return None

    return helper([])

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=argparse.FileType('r'))
    parser.add_argument('proposer', type=str)
    parser.add_argument('resource', type=Resource, choices=[c for c in Resource])
    parser.add_argument('amount', type=int)
    parser.add_argument("--intermediate_resources", type=str,help=','.join([r.value for r in Resource]+['all']))
    args = parser.parse_args()

    if args.intermediate_resources == 'all':
        intermediate_resources = [r for r in Resource if r is not args.optimize]
    else:
        intermediate_resources = [Resource(r) for r in args.intermediate_resources.split(',')]
    intermediate_resources = set(intermediate_resources)
    currency_resources = intermediate_resources.union([Resource.energy])
    buyable_resources = intermediate_resources.union([args.resource])

    gamestate = json.load(args.input)

    tf = TradeFinder(gamestate, args.proposer)
    asks_by_currency = collections.defaultdict(list)
    for partner_name,currency_resource,buyable_resource in tqdm(list(itertools.product(
            tf.friendly_enough_to_trade(), currency_resources, buyable_resources))):
        orders = tf.diplomatic_orders(partner_name, buyable_resource, currency_resource)
        asks = [o for o in orders if o.type == TradeType.ASK]
        asks_by_currency[currency_resource].extend(asks)
    
    solution = fulfill(args.resource, args.amount, Resource.energy, asks_by_currency)
    if solution is None:
        print('No solution found! :(')
    else:
        for offer in solution:
            print(offer)
