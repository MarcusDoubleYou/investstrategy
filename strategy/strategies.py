import json
import pandas as pd

from strategy import preparedata
from strategy.utils import CourseDirection, TradeState, OrderType, remove_key


class StrategyExecutor:
    pass


@DeprecationWarning
class StaticStrategy(object):
    symbol = None
    trade_id = None
    entry = 0.0
    target = 0.0
    stop = 0.0
    quantity = 0.0
    buy_dir = CourseDirection.PRICE_ABOVE
    sell_dir = CourseDirection.PRICE_ABOVE
    buy_order_type = OrderType.MARKET
    sell_order_type = OrderType.MARKET
    state = TradeState.WATCHING
    strategy_type = None

    def __init__(self,
                 symbol=None,
                 target=0.0,
                 stop=0.0,
                 entry=0.0,
                 quantity=0.0,
                 buy_dir=CourseDirection.PRICE_ABOVE,
                 sell_dir=CourseDirection.PRICE_ABOVE,
                 buy_order_type=OrderType.MARKET,
                 sell_order_type=OrderType.MARKET,
                 state=TradeState.WATCHING,
                 trade_id=None,
                 strategy_type=None,
                 trigger="PriceMovement") -> None:

        super().__init__()
        self.trigger = trigger
        self.sell_order_type = sell_order_type
        self.buy_order_type = buy_order_type
        self.strategy_type = strategy_type
        self.tradeId = trade_id
        self.target = target
        self.entry = entry
        self.quantity = quantity
        self.buy_dir = buy_dir
        self.sell_dir = sell_dir
        self.state = state
        self.stop = stop
        self.symbol = symbol

    trigger = "PriceMovement"

    def buy_trigger(self):
        return False

    def sell_trigger(self):
        return False

    def update_dynamic(self, **kwargs):
        print("fetch data for common")
        if kwargs.keys().__contains__('data'):
            self.data = kwargs['data']
            self.data = preparedata.add_features(self.data)
            try:
                self.course = float(self.data['last'][-1:])
                # print(data[:][-1:])
                # print(data['last'][-5:])
                # print("STATE", self.state, " course", self.course)
            except TypeError:
                print("ERROR: getting latest course")
        if kwargs.keys().__contains__('stop'):
            self.stop = kwargs['stop']
        if kwargs.keys().__contains__('exit'):
            self.target = kwargs['ext']
        if kwargs.keys().__contains__('entry'):
            self.entry = kwargs['entry']

    def json(self, log=True):
        j = json.dumps(remove_key(self.__dict__, 'data'))
        if log:
            print(j)
        return j

@DeprecationWarning
class BaseStrategy(object):
    symbol = None
    trade_id = None
    entry = 0.0
    target = 0.0
    stop = 0.0
    quantity = 0.0
    buy_dir = CourseDirection.PRICE_ABOVE
    sell_dir = CourseDirection.PRICE_ABOVE
    buy_order_type = OrderType.MARKET
    sell_order_type = OrderType.MARKET
    state = TradeState.WATCHING
    strategy_type = None
    # dynamic
    gain = 0.0
    course = 0.0
    data = pd.DataFrame()

    def __init__(self,
                 symbol=None,
                 target=0.0,
                 stop=0.0,
                 gain=0.0,
                 entry=0.0,
                 course=0.0,
                 quantity=0.0,
                 buy_dir=CourseDirection.PRICE_ABOVE,
                 sell_dir=CourseDirection.PRICE_ABOVE,
                 buy_order_type=OrderType.MARKET,
                 sell_order_type=OrderType.MARKET,
                 state=TradeState.WATCHING,
                 data=pd.DataFrame(),
                 trade_id=None,
                 strategy_type=None,
                 trigger="PriceMovement") -> None:

        super().__init__()
        self.trigger = trigger
        self.sell_order_type = sell_order_type
        self.buy_order_type = buy_order_type
        self.strategy_type = strategy_type
        self.tradeId = trade_id
        self.target = target
        self.gain = gain
        self.entry = entry
        self.course = course
        self.quantity = quantity
        self.buy_dir = buy_dir
        self.sell_dir = sell_dir
        self.state = state
        self.data = data
        self.stop = stop
        self.symbol = symbol

    trigger = "PriceMovement"

    def buy_trigger(self):
        return False

    def sell_trigger(self):
        return False

    def update_dynamic(self, **kwargs):
        print("fetch data for common")
        if kwargs.keys().__contains__('data'):
            self.data = kwargs['data']
            self.data = preparedata.add_features(self.data)
            try:
                self.course = float(self.data['last'][-1:])
                # print(data[:][-1:])
                # print(data['last'][-5:])
                # print("STATE", self.state, " course", self.course)
            except TypeError:
                print("ERROR: getting latest course")
        if kwargs.keys().__contains__('stop'):
            self.stop = kwargs['stop']
        if kwargs.keys().__contains__('exit'):
            self.target = kwargs['ext']
        if kwargs.keys().__contains__('entry'):
            self.entry = kwargs['entry']

    def json(self, log=True):
        j = json.dumps(remove_key(self.__dict__, 'data'))
        if log:
            print(j)
        return j

@DeprecationWarning
class SimpleMomentumStrategy(BaseStrategy):

    def buy_trigger(self):
        if self.buy_dir == CourseDirection.PRICE_ABOVE:
            if self.course >= self.entry:
                return True
        elif self.buy_dir == CourseDirection.PRICE_ABOVE:
            if self.course <= self.entry:
                return True
        return super().buy_trigger()

    def sell_trigger(self):
        if self.sell_dir == CourseDirection.PRICE_ABOVE:
            if self.course >= self.target:
                return True
        else:
            if self.course <= self.target:
                return True
        return super().sell_trigger()

    def update_dynamic(self, **kwargs):
        super().update_dynamic(**kwargs)


class SimpleMovingAverageStrategy(BaseStrategy):
    _200sma = None
    _50sma = None
    _20sma = None
    _50ema = None
    _20ema = None

    def buy_trigger(self):
        if self.buy_dir == CourseDirection.PRICE_ABOVE:
            if self.course >= self.entry:
                return True
        elif self.buy_dir == CourseDirection.PRICE_ABOVE:
            if self.course <= self.entry:
                return True
        return super().buy_trigger()

    def sell_trigger(self):
        if self.sell_dir == CourseDirection.PRICE_ABOVE:
            if self.course >= self.target:
                return True
        else:
            if self.course <= self.target:
                return True
        return super().sell_trigger()

    def update_dynamic(self, **kwargs):
        super().update_dynamic(**kwargs)
