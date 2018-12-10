import json

from strategy.summary import TradeSummary
from strategy.utils import TradeState, OrderType, ProjectTime

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

    def __init__(self, symbol=None, strategy=None, mock=True, state=TradeState.WATCHING, active=True,
                 bought=None) -> None:
        super().__init__()
        self.bought = bought
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

    def load(self, format_type="json_file", path=None, json_string=None):
        if format_type == "json_file" and path is not None:
            with open(path, "r") as f:
                self = self._convert_from_json(f.read())
        elif json_string is not None:
            self = self._convert_from_json(json_string)
        else:
            raise IOError("Trade cannot be refreshed")
        pass
        return self

    def _convert_from_json(self, j):
        dict = json.loads(j)
        self.active = dict.get('active', self.active)
        self.state = dict.get('state', self.state)
        self.symbol = dict.get('symbol', self.symbol)
        self.created_at = dict.get('created_at', self.created_at)
        self.mock = dict.get('mock', self.mock)
        self.updated_at = dict.get('updated_at', self.updated_at)
        self.state_history = dict.get('state_history', self.state_history)
        self.activity_history = dict.get('activity_history', self.activity_history)
        self.bought = dict.get('bought', self.bought)

        strategy_dict = dict.get('strategy', self.strategy)
        # would fail if loaded without having class init first
        if self.strategy is None:
            self.strategy = TradeStrategy(buy_trigger=strategy_dict.get('buy_trigger'),
                                          sell_trigger=strategy_dict.get('sell_trigger'),
                                          stop=strategy_dict.get('stop_trigger'),
                                          quantity=strategy_dict.get('quantity')
                                          )
        else:
            self.strategy = TradeStrategy(buy_trigger=strategy_dict.get('buy_trigger', self.strategy.buy_trigger),
                                          sell_trigger=strategy_dict.get('sell_trigger', self.strategy.sell_trigger),
                                          stop=strategy_dict.get('stop_trigger', self.strategy.stop_trigger),
                                          quantity=strategy_dict.get('quantity', self.strategy.quantity)
                                          )

        return self

    def refresh(self, format_type="json_file", path=None, json_string=None):
        if format_type == "json_file" and path is not None:
            with open(path, "r") as f:
                self.strategy = self._convert_from_json(f.read()).strategy
        elif json_string is not None:
            self.strategy = self._convert_from_json(json_string).strategy
        else:
            raise IOError("Trade cannot be refreshed")
        pass
        return self


class TradeOrder:
    type = None
    limit = None
    value = None
