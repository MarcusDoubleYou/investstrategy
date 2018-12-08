import json
from collections import namedtuple

from strategy.summary import TradeSummary
from strategy.trigger import TradeTrigger
from strategy.utils import remove_key, TradeState, OrderType, ProjectTime

'''
dynamic parts that can be updated 
'''


class TradeStrategy:
    buy_trigger = None
    buy_order = None
    sell_trigger = None
    sell_order = None
    quantity = 0
    commission = 10
    # TODO should be stop trigger and stop order as well
    stop_trigger = 0

    def __init__(self
                 , buy_trigger
                 , sell_trigger
                 , stop
                 , quantity
                 , buy_order=OrderType.MARKET
                 , sell_order=OrderType.MARKET
                 , commission=10
                 ) \
            -> None:
        super().__init__()
        self.buy_trigger = buy_trigger
        self.sell_trigger = sell_trigger
        self.stop_trigger = stop
        self.quantity = quantity
        self.buy_order = buy_order
        self.sell_order = sell_order
        self.commission = commission

    def to_json(self):
        return self.__dict__


class Trade:
    activity_history = []
    state_history = []
    state = None
    active = False
    strategy: TradeStrategy = None
    mock = True
    symbol = None
    summary = TradeSummary
    created_at = None
    updated_at = None

    def __init__(self, symbol=None, strategy=None, mock=True, state=TradeState.WATCHING, active=True) -> None:
        super().__init__()
        self.state = state
        self.active = active
        self.symbol = symbol
        self.mock = mock
        self.strategy = strategy
        self.symbol = symbol
        self.created_at = ProjectTime().string_time()
        self.updated_at = ProjectTime().string_time()
        self.activity_history = []
        self.state_history = [state]

    def to_json(self, log=False):
        j = json.dumps(self.__dict__, default=lambda o: o.to_json())
        if log:
            print(j)
        return j

    def persist(self, format_type="json_file", path=None):
        if format_type == "json_file" and path is not None:
            with open(path, "w") as f:
                f.write(self.to_json())
        else:
            raise IOError("Trade cannot be written to file")
        pass

    def load(self, format_type="json_file", path=None):
        if format_type == "json_file" and path is not None:
            with open(path, "r") as f:
                self = self._convert_from_json(f.read())

        else:
            raise IOError("Trade cannot be refreshed")
        pass
        return self

    def _convert_from_json(self, j):
        dict = json.loads(j)
        self.active = dict['active']
        self.state = dict['state']
        self.symbol = dict['symbol']
        self.created_at = dict['created_at']
        self.mock = dict['mock']
        self.updated_at = dict['updated_at']
        self.state_history = dict['state_history']
        self.activity_history = dict['activity_history']

        strategy_dict = dict['strategy']
        self.strategy = TradeStrategy(buy_trigger=strategy_dict['buy_trigger'],
                                      sell_trigger=strategy_dict['sell_trigger'],
                                      stop=strategy_dict['stop_trigger'],
                                      quantity=strategy_dict['quantity']
                                      )
        return self

    def refresh(self, format_type="json_file", path=None):
        if format_type == "json_file" and path is not None:
            with open(path, "r") as f:
                self.strategy = self._convert_from_json(f.read()).strategy

        else:
            raise IOError("Trade cannot be refreshed")
        pass
        return self


class TradeOrder:
    type = None
    limit = None
    value = None
