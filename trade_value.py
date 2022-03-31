#! /usr/bin/env python3

import enum
from typing import *

UDENOM = 100000
def udenom(x) -> int:
    return int(x * UDENOM)

TRADE_VALUE_RESOURCE_INCOME_BASE = 50*UDENOM
TRADE_VALUE_RESOURCE = 2*UDENOM
# TRADE_VALUE_RESOURCE_MONTHLY_MULT = 0.5
OFFER_TRADE_MIN_RESOURCE_THRESHOLD = int(0.8*UDENOM)

class Resource(enum.Enum):
    energy = 'energy'
    minerals = 'minerals'
    food = 'food'
    consumer_goods = 'consumer_goods'
    alloys = 'alloys'
    volatile_motes = 'volatile_motes'
    exotic_gases = 'exotic_gases'
    rare_crystals = 'rare_crystals'
    sr_zro = 'sr_zro'
    sr_dark_matter = 'sr_dark_matter'
    nanites = 'nanites'

AI_WEIGHTS = {
    Resource.energy: 1.5,
    Resource.minerals: 1,
    Resource.food: 1,
    Resource.consumer_goods: 5,
    Resource.alloys: 5,
    Resource.volatile_motes: 10,
    Resource.exotic_gases: 10,
    Resource.rare_crystals: 10,
    Resource.sr_zro: 100,
    Resource.sr_dark_matter: 100,
    Resource.nanites: 100,
}

DEFAULT_RESOURCE_CAPS = {
    Resource.energy: 50000,
    Resource.minerals: 15000,
    Resource.food: 15000,
    Resource.consumer_goods: 15000,
    Resource.alloys: 15000,
    Resource.volatile_motes: None,
    Resource.exotic_gases: None,
    Resource.rare_crystals: None,
    Resource.sr_zro: None,
    Resource.sr_dark_matter: None,
    Resource.nanites: None,
}

def trade_value_for_recipient(
    resource: Resource,
    offeredAmount: int,
    # Income, *not* net per month
    senderIncome: float,
    recipientIncome: float,
    recipientTradeWillingness: float, # [0,1]
    recipientCurrentStockpile: float,
    recipientResourceCap: Optional[int],
    debug=False,
):
    rawAIWeight = udenom(AI_WEIGHTS[resource])
    def usableOfferAmount():
        if recipientResourceCap is None:
            return udenom(offeredAmount)

        headRoom = (
            (OFFER_TRADE_MIN_RESOURCE_THRESHOLD * udenom(recipientResourceCap)) // UDENOM
            -
            udenom(recipientCurrentStockpile)
        )

        if debug: print('headRoom', headRoom, headRoom//UDENOM)
        if headRoom > udenom(offeredAmount): # TODO: this inverts the equation in code
            return udenom(offeredAmount)
        elif headRoom <= 0:
            return 0
        else:
            return headRoom

    def adjustedAIWeight():
        adj = rawAIWeight // 10 + UDENOM
        if adj > 2*UDENOM:
            return 2*UDENOM
        if adj < 0:
            return UDENOM
        return adj

    if debug: print('adjustedAIWeight', adjustedAIWeight())
    hedonFactor = (
        ((adjustedAIWeight() * 100000) //
        (((TRADE_VALUE_RESOURCE_INCOME_BASE * 2 + udenom(senderIncome) + udenom(recipientIncome))
        * 100000) //
        ((TRADE_VALUE_RESOURCE_INCOME_BASE * 200000) // 100000))) *
        TRADE_VALUE_RESOURCE
    )

    if debug: print('hedonFactor', hedonFactor, hedonFactor//UDENOM)
    if debug: print(usableOfferAmount(), usableOfferAmount()//UDENOM)

    tradeHedons = (((((hedonFactor // UDENOM) * usableOfferAmount()) // UDENOM) * UDENOM) // 1200000) * udenom(recipientTradeWillingness)

    if debug: print(tradeHedons, tradeHedons//UDENOM, tradeHedons//UDENOM//UDENOM)
    # TODO: one of these UDENOMs should probably disappear, but I don't think it matters unless you have
    # multiple simultaneous sends (or multiple simultaneous receives)
    return tradeHedons // UDENOM // UDENOM

def test_trade_value_for_recipient():
    assert trade_value_for_recipient(
        resource=Resource.alloys,
        offeredAmount=214,
        senderIncome=85.80,
        recipientIncome=199.42,
        recipientTradeWillingness=0.9,
        recipientCurrentStockpile=309,
        recipientResourceCap=25000,
    ) == 12

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('resource', type=Resource, choices=[c for c in Resource])
    parser.add_argument('offeredAmount', type=int)
    parser.add_argument('senderIncome', type=float)
    parser.add_argument('recipientIncome', type=float)
    parser.add_argument('recipientTradeWillingness', type=float)
    parser.add_argument('recipientCurrentStockpile', type=float)
    parser.add_argument('--recipientResourceCap', type=int, default=25000)
    args = parser.parse_args()
    print(trade_value_for_recipient(
        resource=args.resource,
        offeredAmount=args.offeredAmount,
        senderIncome=args.senderIncome,
        recipientIncome=args.recipientIncome,
        recipientTradeWillingness=args.recipientTradeWillingness,
        recipientCurrentStockpile=args.recipientCurrentStockpile,
        recipientResourceCap=args.recipientResourceCap,
    ))