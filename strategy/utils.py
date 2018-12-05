# typical trade life cycle would be 0 -> 1 -> 2 -> 3
import datetime


class TradeState(object):
    WATCHING = "WATCHING"
    PLACED_BUY_ORDER = "PLACED_BUY_ORDER"
    HOLDING = "HOLDING"
    PLACED_SELL_ORDER = "PLACED_SELL_ORDER"
    FINISHED = "FINISHED"
    CANCELED = "CANCELED"


class CourseDirection(object):
    PRICE_BELOW = "price_below"
    PRICE_ABOVE = "price_above"


class OrderType:
    MARKET = "MARKET"
    LIMITED = "LIMITED"
    STOP_LOSS = "STOP_LOSS"


"""
sample use:
json.dumps(remove_key(self.__dict__, 'data'))

"""


class ProjectTime:
    @staticmethod
    def string_time():
        return datetime.datetime.now().ctime()


def remove_key(d, key):
    r = dict(d)
    del r[key]
    return r
