#! /usr/bin/env python3

import collections
import itertools
import json
import math
from tqdm import tqdm
from typing import *

from trade_value import *
from enumerate_trades import *


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=argparse.FileType('r'))
    parser.add_argument('proposer', type=str)
    parser.add_argument('resource', type=Resource, choices=[c for c in Resource])
    parser.add_argument(
        "--currencies",
        type=str,
        help=','.join([r.value for r in Resource]+['all']),
        default='energy,minerals,food,consumer_goods,alloys',
        )
    parser.add_argument("--depth", type=int, default=3)
    args = parser.parse_args()

    if args.currencies == 'all':
        currencies = [r for r in Resource if r is not args.optimize]
    else:
        currencies = [Resource(r) for r in args.currencies.split(',')]

    gamestate = json.load(args.input)
    print(gamestate['date'][0])
    tf = TradeFinder(gamestate, args.proposer)
    for currency in currencies:
        if currency == args.resource:
            continue
        orders = []
        for partner_name in tqdm(list(tf.friendly_enough_to_trade())):
            orders.extend(tf.diplomatic_orders(partner_name, args.resource, currency))
        asks = [o for o in orders if o.type == TradeType.ASK]
        bids = [o for o in orders if o.type == TradeType.BID]

        print(f'{currency.value}')
        for bid in sorted(bids, key=lambda o: o.price())[(-args.depth):]:
            print(f'  {bid}')
        for ask in sorted(asks, key=lambda o: o.price())[:args.depth]:
            print(f'  {ask}')