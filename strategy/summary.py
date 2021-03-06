# todo potentially merge TradeSummary and Trade or add TradeSummary to trade
import json

from strategy.utils import ProjectTime


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
        self.buy_price = float(buy_price)
        self.symbol = symbol
        self.start_time = ProjectTime().string_time()

    def finish(self, sell_price):
        self.end_time = ProjectTime().string_time()
        # self.holding_time = self.end_time - self.start_time
        self.sell_price = float(sell_price)
        self.gain = round(float((self.sell_price - self.buy_price) * int(self.quantity) - self.commission), 3)
        return self

    def to_json(self):
        return self.__dict__

    def json(self, log=True):
        j = json.dumps(self.__dict__)
        if log:
            print(j)
        return j
