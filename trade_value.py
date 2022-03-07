#! /usr/bin/env python3

UDENOM = 100000
tradeWillingness = int(0.90*UDENOM)

TRADE_VALUE_RESOURCE_INCOME_BASE = 50*UDENOM	# used for calculating resource income effect (lower = more value reduction from higher income)
TRADE_VALUE_RESOURCE = 2*UDENOM	# for minerals and energy (scaled by income & need)
# TRADE_VALUE_RESOURCE_MONTHLY_MULT = 0.5 # value of monthly resources is multiplied by this compared to lump-sum
OFFER_TRADE_MIN_RESOURCE_THRESHOLD = int(0.8*UDENOM) # if ai want for an accumulative resource is at least max * this it won't trade away that resource

# TODO: maybe not udenom
proposerIncome = 18415000
proposedToIncome = 12532800

# proposedToCurrentStockpile = 16025*UDENOM
proposedToCurrentStockpile = 279171160
resourceCapForCountry = 25000*UDENOM

offeredAmountRaw = 400
offeredAmount = offeredAmountRaw*UDENOM

rawAIWeight = 1*UDENOM

def usableOfferAmount():
    headRoom = (
        (OFFER_TRADE_MIN_RESOURCE_THRESHOLD * resourceCapForCountry) // UDENOM
        -
        proposedToCurrentStockpile
    )

    print('headRoom', headRoom, headRoom//UDENOM)
    if headRoom > offeredAmount: # TODO: this inverts the equation in code
        return offeredAmount
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

print('adjustedAIWeight', adjustedAIWeight())
hedonFactor = (
    ((adjustedAIWeight() * 100000) //
    (((TRADE_VALUE_RESOURCE_INCOME_BASE * 2 + proposerIncome + proposedToIncome)
    * 100000) //
    ((TRADE_VALUE_RESOURCE_INCOME_BASE * 200000) // 100000))) *
    TRADE_VALUE_RESOURCE
)
# This one comes up with different answers, probably due to different rounding.
# hedonFactor = (
#     2
#     * TRADE_VALUE_RESOURCE
#     * TRADE_VALUE_RESOURCE_INCOME_BASE
#     * adjustedAIWeight()
#     //(2*TRADE_VALUE_RESOURCE_INCOME_BASE + proposedToIncome + proposerIncome)
# )

print('hedonFactor', hedonFactor, hedonFactor//UDENOM)
print(usableOfferAmount(), usableOfferAmount()//UDENOM)

tradeHedons = (((((hedonFactor // UDENOM) * usableOfferAmount()) // UDENOM) * UDENOM) // 1200000) * tradeWillingness

print(tradeHedons, tradeHedons/UDENOM)