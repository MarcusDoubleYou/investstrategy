import pandas as pd
import numpy as np
import unittest

from strategy.domain import TradeStrategy, Trade


class RiskCalTests(unittest.TestCase):

    def test_simple_trade_strategy(self):
        s = TradeStrategy(buy_trigger="hi::>::10.0", sell_trigger="lo::<::11.0", stop=9, quantity=10)
        self.assertIsNotNone(s.to_json())
        print(s.to_json())

    def test_simple_trade(self):
        s = TradeStrategy(buy_trigger="hi::>::10.0", sell_trigger="lo::<::11.0", stop=9, quantity=10)
        t = Trade(symbol="mock", strategy=s, mock=True)
        self.assertIsNotNone(t.to_json())

    def test_to_json(self):
        s = TradeStrategy(buy_trigger="hi::>::10.0", sell_trigger="lo::<::11.0", stop=9, quantity=10)
        t = Trade(symbol="mock", strategy=s, mock=True)
        self.assertIsNotNone(t.to_json())
        print(t.to_json())

    def test_persist_and_load_json(self):
        path = "temp/sample_trade.json"
        path_refresh = "temp/sample_trade_2.json"
        s = TradeStrategy(buy_trigger="hi::>::10.0", sell_trigger="lo::<::11.0", stop=9, quantity=10)
        t = Trade(symbol="mock", strategy=s, mock=True)
        t.persist(path=path)

        refreshed = t.refresh(path=path_refresh)
        self.assertIsNotNone(refreshed)
        self.assertEqual(refreshed.strategy.buy_trigger, "price::>::99.0")
        self.assertEqual(refreshed.strategy.sell_trigger, "price::<::999.0")

    def test_load_json(self):
        path_refresh = "temp/sample_trade_2.json"

        refreshed = Trade().load(path=path_refresh)
        self.assertIsNotNone(refreshed)
        self.assertEqual(refreshed.symbol, "aapl")
        self.assertEqual(refreshed.active, False)
        self.assertEqual(refreshed.mock, False)
        self.assertEqual(refreshed.strategy.buy_trigger, "price::>::99.0")
        self.assertEqual(refreshed.strategy.sell_trigger, "price::<::999.0")


if __name__ == '__main__':
    unittest.main()
