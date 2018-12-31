import unittest

import pandas as pd

from strategy import preparedata
from strategy.trade import TradeStrategy, Trade
from strategy.feeder import MockEmitter
from strategy.test import utils
from strategy.test.mock_emitter import Emitter
from strategy.trader import MockTrader
from strategy.utils import TradeState


class TradingIntegrationTests(unittest.TestCase):

    def tearDown(self):
        utils.clean_temp_directory()
        super().setUp()

    def rand_df(self):
        return Emitter()._data

    def test_trade_buy_sell(self):
        e = MockEmitter()
        strategy = TradeStrategy(buy_trigger="price::>::2.0", sell_trigger="price::>::7.0",
                                 stop_trigger="price::<::5.0",
                                 quantity=10)
        trade = Trade(symbol="mock", strategy=strategy, mock=True)
        trader = MockTrader(trade)
        while e.not_finished() and trader.trade.active:
            trader.follow_course(data=e.emit())

        self.assertFalse(trader.trade.active)
        self.assertEqual(trader.trade.state, TradeState.FINISHED)
        self.assertIsNotNone(trader.trade.state_history)

    def test_trade_dont_buy(self):
        e = MockEmitter()
        strategy = TradeStrategy(buy_trigger="price::>::20.0", sell_trigger="price::>::7.0",
                                 stop_trigger="price::<::5.0",
                                 quantity=10)
        trade = Trade(symbol="mock", strategy=strategy, mock=True)
        trader = MockTrader(trade)
        while e.not_finished() and trader.trade.active:
            trader.follow_course(data=e.emit())

        self.assertTrue(trader.trade.active)
        self.assertEqual(trader.trade.state, TradeState.WATCHING)

    def test_trade_buy_holding(self):
        e = MockEmitter()
        strategy = TradeStrategy(buy_trigger="price::>::2.0", sell_trigger="price::>::20.0",
                                 stop_trigger="price::<::0.5",
                                 quantity=10)
        trade = Trade(symbol="mock", strategy=strategy, mock=True)
        trader = MockTrader(trade)
        while e.not_finished() and trader.trade.active:
            trader.follow_course(data=e.emit())

        self.assertTrue(trader.trade.active)
        self.assertEqual(trader.trade.state, TradeState.HOLDING)
        self.assertIsNotNone(trader.trade.summary)
        self.assertIsNotNone(trader.trade.summary.gain)
        self.assertNotEqual(trader.trade.summary.gain, 0)

    def test_trade_buy_stop_activated(self):
        e = MockEmitter()
        # stop should sell
        strategy = TradeStrategy(buy_trigger="price::>::2.0", sell_trigger="price::>::20.0",
                                 stop_trigger="price::<::10.0",
                                 quantity=10)
        trade = Trade(symbol="mock", strategy=strategy, mock=True)
        trader = MockTrader(trade)
        while e.not_finished() and trader.trade.active:
            trader.follow_course(data=e.emit())

        self.assertFalse(trader.trade.active)
        self.assertEqual(trader.trade.state, TradeState.FINISHED)
        self.assertIsNotNone(trader.trade.summary)
        print(trader.trade.summary.to_json())

    def test_trade_buy_sell_technical_indicator(self):
        df = pd.read_csv("resources/aapl::2018-06-01::1min.csv")
        df = preparedata.add_moving_averages(df)
        e = MockEmitter(data=df)
        # stop should sell
        strategy = TradeStrategy(buy_trigger="sma_200::<::ema_20::type=ti",
                                 sell_trigger="sma_200::>::sma_50::type=technical_indicator",
                                 stop_trigger="last::<::1.0",
                                 quantity=10)
        trade = Trade(symbol="mock", strategy=strategy, mock=True)
        trader = MockTrader(trade)
        while e.not_finished() and trader.trade.active:
            trader.follow_course(data=e.emit())

        self.assertFalse(trader.trade.active)
        self.assertEqual(trader.trade.state, TradeState.FINISHED)
        print(trader.trade.summary.to_json())

    def test_trade_buy_sell_technical_indicator_2(self):
        df = pd.read_csv("resources/2018-12-25-ams-5min.csv")
        # df = pd.read_csv("resources/aapl::2018-06-01::1min.csv")
        df = preparedata.add_moving_averages(df)
        e = MockEmitter(data=df)
        # stop should sell
        strategy = TradeStrategy(buy_trigger="sma_200::<::last::type=ti&&ema_20::<::last::type=ti",
                                 sell_trigger="ema_50::>::last::type=ti",
                                 stop_trigger="last::<::1.0",
                                 quantity=100)
        trade = Trade(symbol="mock", strategy=strategy, mock=True)
        trader = MockTrader(trade)
        while e.not_finished() and trader.trade.active:
            trader.follow_course(data=e.emit())

        self.assertFalse(trader.trade.active)
        self.assertEqual(trader.trade.state, TradeState.FINISHED)
        print(trader.trade.summary.to_json())


if __name__ == '__main__':
    unittest.main()
