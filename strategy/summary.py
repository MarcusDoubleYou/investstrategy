# todo potentially merge TradeSummary and Trade or add TradeSummary to trade
import datetime
import json


class TradeSummary:
    symbol = None
    buy_price = 0.0
    sell_price = 0.0
    quantity = 0.0
    gain = 0.0
    trade_type = "Common Stock"
    commission = 10.00
    start_time = None
    end_time = None
    holding_time = None
    partial = False

    def __init__(self, symbol, buy_price, quantity, commission=10.00) -> None:
        super().__init__()
        self.commission = commission
        self.quantity = quantity
        self.buy_price = buy_price
        self.symbol = symbol
        self.start_time = datetime.datetime.now().ctime()

    def finished(self, sell_price):
        self.end_time = datetime.datetime.now().ctime()
        # self.holding_time = self.end_time - self.start_time
        self.sell_price = sell_price
        self.gain = (sell_price - self.buy_price) * self.quantity - self.commission

    def json(self, log=False):
        j = json.dumps(self.__dict__)
        if log:
            print(j)
        return j

    def to_json(self, log=False):
        j = json.dumps(self.__dict__)
        if log:
            print(j)
        return j
