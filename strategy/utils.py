# typical trade life cycle would be 0 -> 1 -> 2 -> 3
class TradeState(object):
    WATCHING = "watching"
    PLACED_BUY_ORDER = "placed_buy_order"
    HOLDING = "holding"
    PLACED_SELL_ORDER = "placed_sell_order"
    FINISHED = "finished"
    CANCELED = "canceled"


class CourseDirection(object):
    PRICE_BELOW = "price_below"
    PRICE_ABOVE = "price_above"
