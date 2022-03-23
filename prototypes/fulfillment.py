#! /usr/bin/env python3

import collections
from dataclasses import dataclass
import more_itertools

from trade_value import *

@dataclass
class Offer:
    partner: str
    # What you can buy from the partner.
    resource_offered: Resource
    amount_offered: int
    # What you must pay to the partner to buy the above.
    resource_requested: Resource
    amount_requested: int

def is_valid_fulfillment(
    offers: Iterable[Offer],
    sent_resource: Resource,
    bought_resource: Resource,
    bought_resource_amount: int,
    ) -> bool:
    """
    Checks whether a set of trades exchanges sent_resource for some nonzero quantity of
    bought_resource without any net deduction on any resource except for sent_resource.
    """
    net_inventory_change = collections.defaultdict(int)
    for offer in offers:
        net_inventory_change[offer.resource_offered] += offer.amount_offered
        net_inventory_change[offer.resource_requested] -= offer.amount_requested

    return (
        all(
            net_inventory_change[resource] >= 0
            for resource in Resource
            if resource != sent_resource
        )
        and
        net_inventory_change[bought_resource] >= bought_resource_amount
    )

def slow_optimization(
    offers: Set[Offer],
    sent_resource: Resource,
    bought_resource: Resource,
    bought_resource_amount: int,
    ) -> Set[Offer]:
    """
    Finds the cheapest possible fulfillment using a slow exhaustive search.
    """
    valid_fulfillments = [
        fulfillment
        for fulfillment in more_itertools.powerset(offers)
        if is_valid_fulfillment(
            fulfillment,
            sent_resource,
            bought_resource,
            bought_resource_amount,
        )
    ]
    return min(valid_fulfillments, key=trade_value)
