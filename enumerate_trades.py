#!/usr/bin/env python3

from dataclasses import dataclass
import copy
import itertools
import json
import pathlib
from tqdm import tqdm
from typing import *

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

    'fallen_empire_spiritualist': 0.33,
    'fallen_empire_materialist': 0.5,
    'fallen_empire_xenophobe': 0.0,
    'fallen_empire_xenophile': 0.5,
    'awakened_fallen_empire_spiritualist': 0.33,
    'awakened_fallen_empire_materialist': 0.5,
    'awakened_fallen_empire_xenophobe': 0.0,
    'awakened_fallen_empire_xenophile': 0.5,
    'fallen_empire_machine': 0.5,
    'awakened_fallen_empire_machine': 0.5,
    'berserk_fallen_empire_machine': 0.0,
}

class TradeFinder:
    def __init__(self, gamestate, proposer_name: str):
        self.gamestate = gamestate
        countries = {
            k: v
            for k, v in gamestate['country'][0].items()
            if type(v[0]) == dict
        }
        self.countries_by_name = {
            c[0]['name'][0]: c[0]
            for c in countries.values()
        }
        self.ids_by_name = {
            v[0]['name'][0]: k
            for k, v in countries.items()
        }
        self.proposer_name = proposer_name
        self.proposer = self.countries_by_name[proposer_name]
        self.proposer_id = self.ids_by_name[proposer_name]
        self.proposer_resources = resources_for(self.proposer)

    def friendly_enough_to_trade(self):
        if 'relations_manager' in self.proposer:
            communicating_countries = set([
                relation['country'][0]
                for relation in self.proposer['relations_manager'][0]['relation']
                if 'communications' in relation and relation['communications'][0] == 'yes'
            ])
        else:
            communicating_countries = set()

        for name, country in self.countries_by_name.items():
            if name == self.proposer_name:
                continue

            if 'attitude' not in country['ai'][0]:
                # print(f"{name} has no attitude?")
                continue

            if self.ids_by_name[name] not in communicating_countries:
                # print(f"{name} not contacted")
                continue

            attitude_list = country['ai'][0]['attitude'][0]
            attitude_towards_me = [c for c in attitude_list if c['country'][0] == self.proposer_id]
            if len(attitude_towards_me) == 0:
                # print(f"{name} has no attitude towards {self.proposer_name}")
                continue
            assert len(attitude_towards_me) == 1
            attitude_towards_me = attitude_towards_me[0]
            if attitude_towards_me['attitude'][0] in TRADEABLE_STANCES:
                yield name

    def resource_cap_for(self, recipient, resource: Resource):
        if recipient is self.proposer:
            return None
        return DEFAULT_RESOURCE_CAPS[resource]

    def sendable_resources_for(self, sender, resource: Resource):
        if sender is self.proposer:
            return resources_for(sender)[resource]
        return max(0, resources_for(sender)[resource] - 500)

    def generate_minimal_steps(self, sender, recipient, resource: Resource, trade_willingness: float):
        sendable_resources = self.sendable_resources_for(sender, resource)
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
                recipientResourceCap=self.resource_cap_for(recipient, resource), # TODO: read from save file somehow
            )
            if last_val != val:
                yield (offeredAmount, val)
            last_val = val

    def find_maximal_for(self, partner, trade_value: int, resource: Resource):
        partner_sendable_resources = int(self.sendable_resources_for(partner, resource))
        def tvr(resource_back: int) -> int:
            return trade_value_for_recipient(
                resource=resource,
                offeredAmount=resource_back,
                senderIncome=income(partner, resource),
                recipientIncome=income(self.proposer, resource),
                recipientTradeWillingness=1,
                recipientCurrentStockpile=self.proposer_resources[resource],
                recipientResourceCap=None, # resource cap does not apply to proposer valuation
            )

        def predicate(resource_back: int) -> bool:
            val = tvr(resource_back)
            return trade_value - val < 1

        if not predicate(partner_sendable_resources):
            return partner_sendable_resources

        maximal, _ = bisect(0, partner_sendable_resources, predicate)
        return maximal

    def generate_bids(self, partner, resource: Resource, currency: Resource, trade_willingness: float):
        for volume, val in self.generate_minimal_steps(self.proposer, partner, resource, trade_willingness):
            currency_amt = self.find_maximal_for(partner, val, currency)
            if currency_amt is None:
                # TODO: figure out exactly what is happening for these
                continue
            yield Offer(TradeType.BID, resource, partner['name'][0], volume, currency_amt)

    def generate_asks(self, partner, resource: Resource, currency: Resource, trade_willingness: float):
        for currency_amt, val in self.generate_minimal_steps(self.proposer, partner, currency, trade_willingness):
            volume = self.find_maximal_for(partner, val, resource)
            if volume is None or volume == 0:
                # TODO: figure out exactly what is happening for these
                continue
            yield Offer(TradeType.ASK, resource, partner['name'][0], volume, currency_amt)

    def internal_market_orders(self, resource: Resource, market_fee: float, always_show_market: bool):
        if 'internal_market_fluctuations' not in self.gamestate['market'][0]:
            return
        internal_market_infos = self.gamestate['market'][0]['internal_market_fluctuations'][0]
        market_infos = dict(zip(internal_market_infos['country'], internal_market_infos['resources']))
        proposer_market_info = market_infos.get(self.proposer_id, None)
        if proposer_market_info is None: # WTF
            proposer_market_info = {}
        if resource.value in proposer_market_info:
            fluctuation = 1+float(proposer_market_info[resource.value][0])/100
        else:
            fluctuation = 1
        # TODO: make sure MARKET_BASE_PRICES matches up without this blind skip?
        if resource not in MARKET_BASE_PRICES:
            return

        min_qty = 100 // MARKET_BASE_PRICES[resource]
        if fluctuation <= 1 or always_show_market:
            yield Offer(
                TradeType.ASK,
                resource,
                '(internal market)',
                amount=min_qty,
                currency=int(min_qty*MARKET_BASE_PRICES[resource] * fluctuation * (1 + market_fee)),
            )
        if fluctuation >= 1 or always_show_market:
            yield Offer(
                TradeType.BID,
                resource,
                '(internal market)',
                amount=min_qty,
                currency=int(min_qty*MARKET_BASE_PRICES[resource] * fluctuation * (1 - market_fee)),
            )

    def diplomatic_orders(self, partner_name: str, resource: Resource, currency: Resource):
        personality = self.countries_by_name[partner_name]['personality'][0]
        if personality not in PERSONALITY_TRADE_WILLINGNESS:
            print(f"{partner_name} has unknown personality {personality}")
            print()
            return
        trade_willingness = PERSONALITY_TRADE_WILLINGNESS[personality]
        partner = self.countries_by_name[partner_name]
        yield from self.generate_bids(partner, resource, currency, trade_willingness)
        yield from self.generate_asks(partner, resource, currency, trade_willingness)

    def proposer_usable_stockpiles(self):
            # TODO: handle more gracefully
        proposer_stockpiles = {}
        for resource in Resource:
            stock = t.proposer_resources[resource]
            # print(f"{resource}: {proposer['name'][0]} has {stock} + {balance(proposer,resource)} {resource.value}")
            if balance(t.proposer, resource) < 0:
                stock += balance(t.proposer, resource)
                # print(f'  (effectively {stock})')
            proposer_stockpiles[resource] = stock
        return proposer_stockpiles



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


class TradeType(enum.Enum):
    BID = 'BID'
    ASK = 'ASK'

@dataclass
class Offer:
    type: TradeType
    resource: Resource
    who: str
    amount: int
    currency: int

    def price(self) -> float:
        return self.currency / self.amount

    def __str__(self):
        return f"{self.type.value} {self.resource.value} {self.price():3.2f} {self.amount} {self.currency} {self.who}"


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

def profit(bid: Offer, ask: Offer):
    assert bid.type == TradeType.BID
    assert ask.type == TradeType.ASK
    return bid.currency - ask.currency

def find_execution_plan(
        matches: List[Tuple[Offer, Offer]],
        currency: Resource,
        proposer_stockpiles: Dict[Resource, float],
        sendable_resources_by_country: Dict[str, Dict[Resource, float]],
        ) -> List[Tuple[Offer, Offer]]:
    proposer_stockpiles = copy.deepcopy(proposer_stockpiles)
    sendable_resources_by_country = copy.deepcopy(sendable_resources_by_country)
    matches = sorted(matches, key=lambda m: profit(m[0], m[1]), reverse=True)
    for bid,ask in matches:
        resource = bid.resource
        assert ask.resource == resource
        if proposer_stockpiles[resource] < bid.amount:
            continue
        if sendable_resources_by_country[bid.who][currency] < bid.currency:
            continue

        if proposer_stockpiles[currency] < ask.currency:
            continue
        if sendable_resources_by_country[ask.who][resource] < ask.amount:
            continue

        # print(proposer_stockpiles)
        # print(bid.who, sendable_resources_by_country[bid.who])
        # print(ask.who, sendable_resources_by_country[ask.who])
        # print()

        yield bid,ask

        # Note that we only deduct resources here.
        proposer_stockpiles[resource] -= bid.amount
        proposer_stockpiles[currency] -= ask.currency
        sendable_resources_by_country[bid.who][currency] -= bid.currency
        sendable_resources_by_country[ask.who][resource] -= ask.amount

    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("save_file_json", type=pathlib.Path, help="Save file, but converted to JSON")
    parser.add_argument("proposer", type=str)
    parser.add_argument("resources", type=str,help=','.join([r.value for r in Resource]+['all']))
    parser.add_argument("--print_full_book", action="store_true")
    parser.add_argument("--book_size", type=int, default=3)
    parser.add_argument("--matches_to_show", type=int, default=0)
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--market_fee", type=float, default=0.3)
    parser.add_argument("--always_show_market", action="store_true")
    parser.add_argument("--optimize", type=Resource, default=Resource.energy)
    parser.add_argument("--submit_socket", type=pathlib.Path, default=None)
    args = parser.parse_args()

    if args.resources == 'all':
        resources_to_check = [r for r in Resource if r is not args.optimize]
    else:
        resources_to_check = [Resource(r) for r in args.resources.split(',')]

    with open(args.save_file_json) as f:
        gamestate = json.load(f)

    t = TradeFinder(gamestate, args.proposer)
    diplomatic_orders = []
    for partner_name,resource in tqdm(list(itertools.product(t.friendly_enough_to_trade(), resources_to_check))):
        diplomatic_orders.extend(t.diplomatic_orders(partner_name, resource, args.optimize))
    market_orders = []
    for resource in resources_to_check:
        market_orders.extend(t.internal_market_orders(resource, args.market_fee, args.always_show_market))
    all_orders = diplomatic_orders + market_orders

    proposer_stockpiles = t.proposer_usable_stockpiles()

    all_bids = [o for o in all_orders if o.type == TradeType.BID and o.amount <= proposer_stockpiles[o.resource]]
    all_asks = [o for o in all_orders if o.type == TradeType.ASK]

    def executable(bid: Offer, ask: Offer):
        assert bid.type == TradeType.BID
        assert ask.type == TradeType.ASK
        return (
            (bid.resource == ask.resource) and
            (bid.amount <= ask.amount) and
            (bid.who != ask.who) and
            (bid.amount <= proposer_stockpiles[bid.resource]) and
            (ask.currency <= proposer_stockpiles[args.optimize])
        )

    date = gamestate['date'][0]
    print(f'DATE: {date}')
    print(f'{len(all_bids)} bids, {len(all_asks)} asks')

    for resource in resources_to_check:
        bids = [o for o in all_bids if o.resource == resource]
        asks = [o for o in all_asks if o.resource == resource]
        print(f'{resource.value}: {len(bids)} bids, {len(asks)} asks')
        for bid in sorted(bids, key=lambda o: o.price())[-args.book_size:]:
            print('  ', bid)
        for ask in sorted(asks, key=lambda o: o.price())[:args.book_size]:
            print('  ', ask)

    matches = []
    for resource in tqdm(resources_to_check):
        bids = [o for o in diplomatic_orders if o.type == TradeType.BID and o.resource == resource]
        asks = [o for o in diplomatic_orders if o.type == TradeType.ASK and o.resource == resource]

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

    sendable_resources_by_country = {
        name: {r: t.sendable_resources_for(t.countries_by_name[name], r) for r in Resource}
        for name in t.friendly_enough_to_trade()
    }

    execution_plan = list(find_execution_plan(
        matches,
        args.optimize,
        proposer_stockpiles,
        sendable_resources_by_country,
        ))
    print('Execution plan:')
    for bid,ask in execution_plan:
        print(bid)
        print(ask)
        print(min(bid.amount, ask.amount), profit(bid, ask))
        print()

    if args.submit_socket is not None:
        print('SUBMITTING FOR EXECUTION!')
        import socket
        for bid,ask in tqdm(execution_plan):
            bid_cmd = f'{t.ids_by_name[bid.who]} {bid.resource.value} {bid.amount} {args.optimize.value} {bid.currency}'
            ask_cmd = f'{t.ids_by_name[ask.who]} {args.optimize.value} {ask.currency} {ask.resource.value} {ask.amount}'

            for line in [bid_cmd, ask_cmd]:
                # Open unix domain socket to server
                sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                sock.connect(str(args.submit_socket))
                sock.sendall((line+'\n').encode('utf-8'))
                sock.close()


    if args.print_full_book:
        for o in sorted(all_orders, key=lambda o: o.price()):
            print(o)