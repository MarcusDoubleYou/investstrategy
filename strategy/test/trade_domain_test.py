import pandas as pd
import numpy as np
import unittest
import os, shutil

from strategy import trader
from strategy.domain import TradeStrategy, Trade
from strategy.test import utils
from strategy.trader import MockTrader, MarketDataFeederType, TraderConfig
from strategy.utils import ProjectTime


class TradeDomainTest(unittest.TestCase):

    def tearDown(self):
        utils.clean_temp_directory()
        super().setUp()

    def test_time(self):
        self.assertIsNotNone(ProjectTime().string_time())

    def test_simple_trade_strategy(self):
        s = TradeStrategy(buy_trigger="hi::>::10.0", sell_trigger="lo::<::11.0", stop_trigger="lo::<::11.0",
                          quantity=10)
        self.assertIsNotNone(s.to_json())
        print(s.to_json())

    def test_trader_config(self):
        s = TradeStrategy(buy_trigger="hi::>::10.0", sell_trigger="lo::<::11.0", stop_trigger="lo::<::11.0",
                          quantity=10)
        t = Trade(symbol="lee", strategy=s, mock=True)
        trader = MockTrader(t)
        self.assertIsNotNone(trader)
        self.assertEqual(trader.config.env, "test")
        self.assertEqual(trader.config.feeder_type, MarketDataFeederType.MOCK_DATA)
        self.assertEqual(trader.config.symbol, "lee")

    def test_trader_custom_config(self):
        s = TradeStrategy(buy_trigger="hi::>::10.0", sell_trigger="lo::<::11.0", stop_trigger="lo::<::11.0",
                          quantity=10)
        t = Trade(symbol="lee", strategy=s)
        config = TraderConfig(env="dev", feeder_type=MarketDataFeederType.REAL_DATA_REPLAY,
                              market_data_interval="5min", market_data_pull_interval_sec=10)
        trader = MockTrader(t, config)
        self.assertIsNotNone(trader)
        self.assertEqual(trader.config.env, config.env)
        self.assertEqual(trader.config.feeder_type, config.feeder_type)
        self.assertEqual(trader.config.symbol, config.symbol)


    def test_simple_trade(self):
        s = TradeStrategy(buy_trigger="hi::>::10.0", sell_trigger="lo::<::11.0", stop_trigger="lo::<::11.0",
                          quantity=10)
        t = Trade(symbol="mock", strategy=s, mock=True)
        self.assertIsNotNone(t.to_json())

    def test_to_json(self):
        s = TradeStrategy(buy_trigger="hi::>::10.0", sell_trigger="lo::<::11.0", stop_trigger="lo::<::11.0",
                          quantity=10)
        t = Trade(symbol="mock", strategy=s, mock=True)
        self.assertIsNotNone(t.to_json())
        print(t.to_json())
        t.persist("temp")

    def test_default_config(self):
        config = trader.default_config()
        self.assertIsNotNone(config)
        self.assertEqual(config.env, "test")

    def test_persist_and_load_json(self):
        path = "temp/"
        s = TradeStrategy(buy_trigger="hi::>::10.0", sell_trigger="lo::<::11.0", stop_trigger="lo::<::11.0",
                          quantity=10)
        t = Trade(symbol="mock", strategy=s, mock=True)
        t.persist(path=path)

        refreshed = t.refresh()
        self.assertIsNotNone(refreshed)
        self.assertEqual(refreshed.strategy.buy_trigger, s.buy_trigger)
        self.assertEqual(refreshed.strategy.sell_trigger, s.sell_trigger)
        self.assertEqual(refreshed.strategy.stop_trigger, s.stop_trigger)

    def test_persist_and_load_json_different_file(self):
        path = "temp/"
        path_refresh = "resources/sample_trade_2.json"
        s = TradeStrategy(buy_trigger="hi::>::10.0", sell_trigger="lo::<::11.0", stop_trigger="lo::<::11.0",
                          quantity=10)
        t = Trade(symbol="mock", strategy=s, mock=True)
        t.persist(path=path)

        refreshed = t.refresh(path=path_refresh)
        self.assertIsNotNone(refreshed)
        self.assertEqual(refreshed.strategy.buy_trigger, "price::>::99.0")
        self.assertEqual(refreshed.strategy.sell_trigger, "price::<::999.0")
        self.assertEqual(refreshed.strategy.stop_trigger, "price::>::555.0")

    def test_load_json_file(self):
        path_load = "resources/sample_trade_2.json"

        refreshed = Trade().load(path=path_load)
        # refreshed = Trade(symbol='a').load(path=path_load)
        self.assertIsNotNone(refreshed)
        self.assertEqual(refreshed.symbol, "aapl")
        self.assertEqual(refreshed.active, False)
        self.assertEqual(refreshed.mock, False)
        self.assertEqual(refreshed.strategy.buy_trigger, "price::>::99.0")
        self.assertEqual(refreshed.strategy.sell_trigger, "price::<::999.0")
        self.assertIsNotNone(refreshed.trade_id)
        self.assertFalse(refreshed.trade_id.__contains__("None"))

    def test_load_json_string(self):
        path_load = "resources/sample_trade_2.json"
        with open(path_load, "r") as f:
            json_body = f.read()
            refreshed = Trade().load(json_string=json_body)

            self.assertIsNotNone(refreshed)
            self.assertEqual(refreshed.symbol, "aapl")
            self.assertEqual(refreshed.active, False)
            self.assertEqual(refreshed.mock, False)
            self.assertEqual(refreshed.strategy.buy_trigger, "price::>::99.0")
            self.assertEqual(refreshed.strategy.sell_trigger, "price::<::999.0")

    def test_refresh_json_string(self):
        path_refresh = "resources/sample_trade_2.json"

        s = TradeStrategy(buy_trigger="hi::>::10.0", sell_trigger="lo::<::11.0", stop_trigger="lo::<::11.0",
                          quantity=10)
        t = Trade(symbol="mock", strategy=s, mock=True)

        with open(path_refresh, "r") as f:
            json_body = f.read()
            refreshed = t.refresh(json_string=json_body)
            self.assertIsNotNone(refreshed)
            self.assertEqual(refreshed.strategy.buy_trigger, "price::>::99.0")
            self.assertEqual(refreshed.strategy.sell_trigger, "price::<::999.0")
            self.assertEqual(refreshed.strategy.stop_trigger, "price::>::555.0")


if __name__ == '__main__':
    unittest.main()
