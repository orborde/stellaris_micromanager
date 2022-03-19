#!/usr/bin/env python3

import argparse
from dataclasses import dataclass
import itertools
import json
import pathlib

from tqdm import tqdm

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
PERSONALITY_TRADE_WILLINGNESS = {
    'honorbound_warriors': 0.7,
    'evangelising_zealots': 0.75,
    'erudite_explorers': 0.9,
    'spiritual_seekers': 0.9,
    'ruthless_capitalists': 1.0,
    'peaceful_traders': 1.0,
    'hegemonic_imperialists': 0.8,
    'slaving_despots': 0.8,
    'decadent_hierarchy': 0.9,
    'democratic_crusaders': 0.9,
    'harmonious_hierarchy': 0.9,
    'federation_builders': 0.95,
    'xenophobic_isolationists': 0.5,
    'fanatic_purifiers': 0.5,
    'hive_mind': 0.7,
    'devouring_swarm': 0.0,
    'migrating_flock': 1.1,
    'metalhead': 0.0,
    'machine_intelligence': 0.8,
    'assimilators': 0.5,
    'exterminators': 1.0,
    'servitors': 0.9,
    'fanatic_befrienders': 1.0,
    'became_the_crisis': 0.5,
}


parser = argparse.ArgumentParser()
parser.add_argument("save_file_json", type=pathlib.Path, help="Save file, but converted to JSON")
parser.add_argument("proposer", type=str)
parser.add_argument("resources", type=str,help=','.join([r.value for r in Resource]+['all']))
parser.add_argument("--print_full_book", action="store_true")
parser.add_argument("--book_size", type=int, default=3)
parser.add_argument("--matches_to_show", type=int, default=3)
parser.add_argument("--progress", action="store_true")
parser.add_argument("--market_fee", type=float, default=0.3)
parser.add_argument("--always_show_market", action="store_true")
parser.add_argument("--optimize", type=Resource, default=Resource.energy)
args = parser.parse_args()

if args.resources == 'all':
    resources = [r for r in Resource if r is not args.optimize]
else:
    resources = [Resource(r) for r in args.resources.split(',')]
# print('Processing resource list:', [r.value for r in resources])

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

if 'relations_manager' in proposer:
    communicating_countries = set([
        relation['country'][0]
        for relation in proposer['relations_manager'][0]['relation']
        if 'communications' in relation and relation['communications'][0] == 'yes'
    ])
else:
    communicating_countries = set()

friendly_enough_to_trade = []
for name, country in countries_by_name.items():
    if name == args.proposer:
        continue

    if 'attitude' not in country['ai'][0]:
        # print(f"{name} has no attitude?")
        continue

    if ids_by_name[name] not in communicating_countries:
        # print(f"{name} not contacted")
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

def balance(country, resource: Resource):
    return sum(
        float(d[0][resource.value][0])
        for d in country['budget'][0]['current_month'][0]['balance'][0].values()
        if d[0] is not None and resource.value in d[0])


def resources_for(country):
    raw_resource_dict = country['modules'][0]['standard_economy_module'][0]['resources'][0]
    ret = {}
    for resource in Resource:
        if resource.value in raw_resource_dict:
            ret[resource] = float(raw_resource_dict[resource.value][0])
        else:
            ret[resource] = 0
    return ret


proposer_resources = resources_for(proposer)

def bisect(lo: int, hi: int, predicate):
    assert predicate(hi)
    assert not predicate(lo)
    while lo+1 < hi:
        mid = (lo + hi) // 2
        if predicate(mid):
            hi = mid
        else:
            lo = mid
    assert lo+1 == hi
    return lo,hi

def resource_cap_for(recipient, resource: Resource):
    if recipient is proposer:
        return None
    return DEFAULT_RESOURCE_CAPS[resource]

def sendable_resources_for(sender, resource: Resource):
    if sender is proposer:
        return resources_for(sender)[resource]
    return max(0, resources_for(sender)[resource] - 500)

def generate_minimal_steps(sender, recipient, resource: Resource, trade_willingness: float):
    sendable_resources = sendable_resources_for(sender, resource)
    recipient_resources = resources_for(recipient)
    last_val = 0
    for offeredAmount in range(int(sendable_resources)+1):
        val = trade_value_for_recipient(
            resource=resource,
            offeredAmount=offeredAmount,
            senderIncome=income(sender, resource),
            recipientIncome=income(recipient, resource),
            recipientTradeWillingness=trade_willingness,
            recipientCurrentStockpile=recipient_resources[resource],
            recipientResourceCap=resource_cap_for(recipient, resource), # TODO: read from save file somehow
        )
        if last_val != val:
            yield (offeredAmount, val)
        last_val = val

def find_maximal_for(partner, trade_value: int, resource: Resource):
    partner_sendable_resources = int(sendable_resources_for(partner, resource))
    def tvr(resource_back: int) -> int:
        return trade_value_for_recipient(
            resource=resource,
            offeredAmount=resource_back,
            senderIncome=income(partner, resource),
            recipientIncome=income(proposer, resource),
            recipientTradeWillingness=1,
            recipientCurrentStockpile=proposer_resources[resource],
            recipientResourceCap=None, # resource cap does not apply to proposer valuation
        )

    def predicate(resource_back: int) -> bool:
        val = tvr(resource_back)
        return trade_value - val < 1

    if not predicate(partner_sendable_resources):
        return partner_sendable_resources

    maximal, _ = bisect(0, partner_sendable_resources, predicate)
    return maximal

class TradeType(enum.Enum):
    BID = 'BID'
    ASK = 'ASK'

@dataclass
class Offer:
    type: TradeType
    resource: Resource
    who: str
    amount: int
    energy: int

    def price(self) -> float:
        return self.energy / self.amount

    def __str__(self):
        return f"{self.type.value} {self.resource.value} {self.price():3.2f} {self.amount} {self.energy} {self.who}"


def generate_bids(partner, resource: Resource, trade_willingness: float):
    for volume, val in generate_minimal_steps(proposer, partner, resource, trade_willingness):
        energy_amt = find_maximal_for(partner, val, args.optimize)
        if energy_amt is None:
            # TODO: figure out exactly what is happening for these
            continue
        yield Offer(TradeType.BID, resource, partner['name'][0], volume, energy_amt)

def generate_asks(partner, resource: Resource, trade_willingness: float):
    for energy_amt, val in generate_minimal_steps(proposer, partner, args.optimize, trade_willingness):
        volume = find_maximal_for(partner, val, resource)
        if volume is None or volume == 0:
            # TODO: figure out exactly what is happening for these
            continue
        yield Offer(TradeType.ASK, resource, partner['name'][0], volume, energy_amt)

MARKET_BASE_PRICES = {
    Resource.minerals: 1,
    Resource.food: 1,
    Resource.consumer_goods: 2,
    Resource.alloys: 4,
    Resource.volatile_motes: 10,
    Resource.exotic_gases: 10,
    Resource.rare_crystals: 10,
    Resource.sr_zro: 20,
    Resource.sr_dark_matter: 20,
}
def internal_market_orders():
    if 'internal_market_fluctuations' not in gamestate['market'][0]:
        return []
    internal_market_infos = gamestate['market'][0]['internal_market_fluctuations'][0]
    market_infos = dict(zip(internal_market_infos['country'], internal_market_infos['resources']))
    proposer_market_info = market_infos.get(proposer_id, None)
    if proposer_market_info is None: # WTF
        proposer_market_info = {}
    for resource in resources:
        if resource.value in proposer_market_info:
            fluctuation = 1+float(proposer_market_info[resource.value][0])/100
        else:
            fluctuation = 1
        # TODO: make sure MARKET_BASE_PRICES matches up without this blind skip?
        if resource not in MARKET_BASE_PRICES:
            continue

        min_qty = 100 // MARKET_BASE_PRICES[resource]
        if fluctuation <= 1 or args.always_show_market:
            yield Offer(
                TradeType.ASK,
                resource,
                '(internal market)',
                amount=min_qty,
                energy=int(min_qty*MARKET_BASE_PRICES[resource] * fluctuation * (1 + args.market_fee)),
            )
        if fluctuation >= 1 or args.always_show_market:
            yield Offer(
                TradeType.BID,
                resource,
                '(internal market)',
                amount=min_qty,
                energy=int(min_qty*MARKET_BASE_PRICES[resource] * fluctuation * (1 - args.market_fee)),
            )

orders = []
orders.extend(internal_market_orders())
for partner_name,resource in tqdm(list(itertools.product(friendly_enough_to_trade, resources))):
    personality = countries_by_name[partner_name]['personality'][0]
    if personality not in PERSONALITY_TRADE_WILLINGNESS:
        print(f"{partner_name} has unknown personality {personality}")
        print()
        continue
    trade_willingness = PERSONALITY_TRADE_WILLINGNESS[personality]
    if args.progress:
        print(partner_name, resource.value, ids_by_name[partner_name], personality, trade_willingness)
    partner = countries_by_name[partner_name]
    bids = list(generate_bids(partner, resource, trade_willingness))
    asks = list(generate_asks(partner, resource, trade_willingness))
    if args.progress:
        print(f"{len(bids)} bids, {len(asks)} asks")
    orders.extend(bids)
    orders.extend(asks)

# TODO: handle more gracefully
proposer_stockpiles = {}
for resource in Resource:
    stock = proposer_resources[resource]
    # print(f"{resource}: {proposer['name'][0]} has {stock} + {balance(proposer,resource)} {resource.value}")
    if balance(proposer, resource) < 0:
        stock += balance(proposer, resource)
        # print(f'  (effectively {stock})')
    proposer_stockpiles[resource] = stock

all_bids = [o for o in orders if o.type == TradeType.BID and o.amount <= proposer_stockpiles[o.resource]]
all_asks = [o for o in orders if o.type == TradeType.ASK]

def executable(bid: Offer, ask: Offer):
    assert bid.type == TradeType.BID
    assert ask.type == TradeType.ASK
    return (
        (bid.resource == ask.resource) and
        (bid.amount <= ask.amount) and
        (bid.who != ask.who) and
        (bid.amount <= proposer_stockpiles[bid.resource]) and
        (ask.energy <= proposer_stockpiles[args.optimize])
    )

def profit(bid: Offer, ask: Offer):
    assert bid.type == TradeType.BID
    assert ask.type == TradeType.ASK
    assert executable(bid, ask)
    return bid.energy - ask.energy

date = gamestate['date'][0]
print(f'DATE: {date}')
print(f'{len(all_bids)} bids, {len(all_asks)} asks')

matches = []
for resource in tqdm(resources):
    bids = [o for o in all_bids if o.resource == resource]
    asks = [o for o in all_asks if o.resource == resource]
    print(f'{resource.value}: {len(bids)} bids, {len(asks)} asks')
    for bid in sorted(bids, key=lambda o: o.price(), reverse=True)[:args.book_size]:
        print('  ', bid)
    for ask in sorted(asks, key=lambda o: o.price())[:args.book_size]:
        print('  ', ask)

    matches.extend(
        (bid, ask)
        for bid,ask in itertools.product(bids, asks)
        if executable(bid, ask) and profit(bid, ask) > 0
    )

matches.sort(key=lambda m: profit(m[0], m[1]), reverse=True)
print(f'{len(matches)} profitable matches')
for bid,ask in reversed(matches[:args.matches_to_show]):
    print(bid)
    print(ask)
    print(min(bid.amount, ask.amount), profit(bid, ask))
    print()

if args.print_full_book:
    for o in sorted(orders, key=lambda o: o.price()):
        print(o)