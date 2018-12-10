import unittest

from strategy.domain import TradeStrategy, Trade
from strategy.feeder import MockEmitter
from strategy.test.mock_emitter import Emitter
from strategy.trader import MockTrader
from strategy.utils import TradeState


class TradingIntegrationTests(unittest.TestCase):

    def rand_df(self):
        return Emitter()._data

    def test_trade_buy_sell(self):
        e = MockEmitter()
        strategy = TradeStrategy(buy_trigger="price::>::2.0", sell_trigger="price::>::7.0", stop="price::<::5.0",
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
        strategy = TradeStrategy(buy_trigger="price::>::20.0", sell_trigger="price::>::7.0", stop="price::<::5.0",
                                 quantity=10)
        trade = Trade(symbol="mock", strategy=strategy, mock=True)
        trader = MockTrader(trade)
        while e.not_finished() and trader.trade.active:
            trader.follow_course(data=e.emit())

        self.assertTrue(trader.trade.active)
        self.assertEqual(trader.trade.state, TradeState.WATCHING)

    def test_trade_buy_holding(self):
        e = MockEmitter()
        strategy = TradeStrategy(buy_trigger="price::>::2.0", sell_trigger="price::>::20.0", stop="price::<::0.5",
                                 quantity=10)
        trade = Trade(symbol="mock", strategy=strategy, mock=True)
        trader = MockTrader(trade)
        while e.not_finished() and trader.trade.active:
            trader.follow_course(data=e.emit())

        self.assertTrue(trader.trade.active)
        self.assertEqual(trader.trade.state, TradeState.HOLDING)

    def test_trade_buy_stop_activated(self):
        e = MockEmitter()
        # stop should sell
        strategy = TradeStrategy(buy_trigger="price::>::2.0", sell_trigger="price::>::20.0", stop="price::<::10.0",
                                 quantity=10)
        trade = Trade(symbol="mock", strategy=strategy, mock=True)
        trader = MockTrader(trade)
        while e.not_finished() and trader.trade.active:
            trader.follow_course(data=e.emit())

        self.assertFalse(trader.trade.active)
        self.assertEqual(trader.trade.state, TradeState.FINISHED)


if __name__ == '__main__':
    unittest.main()
