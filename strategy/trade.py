import json

from strategy.summary import TradeSummary
from strategy.utils import TradeState, OrderType, ProjectTime
import random

'''
dynamic parts that can be updated 
'''


class StrategyName:
    DAY_BULL = "DAY_BULL"
    DAY_BEAR = "DAY_BEAR"
    GALPER = "GALPER"
    SHORT_SQUEEZE = "SHORT_SQUEEZE"


# TODO gain
class TradeStrategy:
    buy_trigger = None
    buy_order = None
    sell_trigger = None
    sell_order = None
    quantity = 0
    commission = 10
    # TODO should be stop trigger and stop order as well
    stop_trigger = 0
    name = None
    description = None

    def __init__(self
                 , buy_trigger
                 , sell_trigger
                 , stop_trigger
                 , quantity
                 , buy_order=OrderType.MARKET
                 , sell_order=OrderType.MARKET
                 , commission=10
                 , name=StrategyName.DAY_BEAR
                 , description=None
                 ) \
            -> None:
        super().__init__()
        self.name = name
        self.buy_trigger = buy_trigger
        self.sell_trigger = sell_trigger
        self.stop_trigger = stop_trigger
        self.quantity = quantity
        self.buy_order = buy_order
        self.sell_order = sell_order
        self.commission = commission
        self.description = description

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
    trade_id = None
    _path = None

    def __init__(self, symbol=None, strategy=None, mock=True, state=TradeState.WATCHING, active=True,
                 buy_price=None, trade_id=None) -> None:
        super().__init__()

        self.buy_price = buy_price
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
        self.trade_id = trade_id
        if self.trade_id is None and symbol is not None:
            self.trade_id = "trade::" + str(self.symbol) + "::" + str(
                round(random.Random().random() * 1000000000000))

    def to_json(self, log=False):
        j = json.dumps(self.__dict__, default=lambda o: o.to_json())
        if log:
            print(j)
        return j

    def persist(self, path=None, format_type="json_file"):
        if format_type == "json_file":
            with open(self.get_name(path), "w") as f:
                f.write(self.to_json())
        else:
            raise IOError("Trade cannot be written to file")
        pass

    def get_name(self, path=None, format=".json"):
        """
        can overwrite file if not specified
        :param path:
        :param format:
        :return:
        """
        # if full path is given it will be use
        if path is not None and str(path).endswith(format):
            self._path = path
        else:
            if path is None and self._path is None:
                self._path = self.trade_id + format
            elif path is not None and self._path is None:
                self._path = str(path) + "/" + self.trade_id + format

        return self._path

    def load(self, format_type="json_file", path=None, json_string=None):
        if json_string is not None:
            self = self._convert_from_json(json_string)
        elif format_type == "json_file":
            with open(self.get_name(path), "r") as f:
                self = self._convert_from_json(f.read())
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
        self.buy_price = dict.get('buy_price', self.buy_price)
        self.trade_id = dict.get('trade_id', self.trade_id)

        # in case trade id was not supplied through json file
        if self.trade_id is None:
            self.trade_id = "trade::" + str(self.symbol) + "::" + str(
                round(random.Random().random() * 1000000000000))

        strategy_dict = dict.get('strategy', self.strategy)
        # would fail if loaded without having class init first
        if self.strategy is None:
            self.strategy = TradeStrategy(buy_trigger=strategy_dict.get('buy_trigger'),
                                          sell_trigger=strategy_dict.get('sell_trigger'),
                                          stop_trigger=strategy_dict.get('stop_trigger'),
                                          quantity=strategy_dict.get('quantity'),
                                          name=strategy_dict.get('name'),
                                          description=strategy_dict.get('description')
                                          )
        else:
            self.strategy = TradeStrategy(buy_trigger=strategy_dict.get('buy_trigger', self.strategy.buy_trigger),
                                          sell_trigger=strategy_dict.get('sell_trigger', self.strategy.sell_trigger),
                                          stop_trigger=strategy_dict.get('stop_trigger', self.strategy.stop_trigger),
                                          quantity=strategy_dict.get('quantity', self.strategy.quantity),
                                          name=strategy_dict.get(self.strategy.name),
                                          description=strategy_dict.get(self.strategy.description)
                                          )

        return self

    def refresh(self, format_type="json_file", path=None, json_string=None):
        if json_string is not None:
            self.strategy = self._convert_from_json(json_string).strategy
        elif format_type == "json_file":
            with open(self.get_name(path), "r") as f:
                self.strategy = self._convert_from_json(f.read()).strategy
        else:
            raise IOError("Trade cannot be refreshed")
        pass
        return self

    # todo rethink if this should live inside of trade
    def finish(self, sell_price):
        summary = TradeSummary(symbol=self.symbol, buy_price=self.buy_price, quantity=self.strategy.quantity,
                               commission=self.strategy.commission)
        summary.finish(sell_price)
        self.summary = summary
        return summary


class TradeOrder:
    type = None
    limit = None
    value = None
