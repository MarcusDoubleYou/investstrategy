import unittest

from strategy.domain import Trade
from strategy.feeder import MockEmitter
from strategy.riskcalculator import StrategyEval
from strategy.test import utils
from strategy.trader import MockTrader


class TradingLifeCycle(unittest.TestCase):

    def tearDown(self):
        utils.clean_temp_directory()
        super().setUp()

    def test_full_lifecycle_mock(self):
        e = MockEmitter()
        eval2 = StrategyEval()
        eval2.eval_with_loss_of_investment(20, 30, 2000, "25%", commission=20)
        strategy = eval2.create_trade_strategy()
        trade = Trade(symbol="mock", strategy=strategy, mock=True)
        trader = MockTrader(trade)

        while e.not_finished() and trader.trade.active:
            trader.follow_course(data=e.emit())

        self.assertIsNotNone(trader.trade.summary)
        self.assertIsNotNone(trader.trade.summary.gain)

    def test_full_lifecycle_apple(self):
        e = MockEmitter(data_path="resources/aapl::2018-06-01::1min.csv")
        eval2 = StrategyEval()
        eval2.eval_with_loss_of_investment(188.2, "3%", 2000, "10%", commission=10)
        strategy = eval2.create_trade_strategy()
        trade = Trade(symbol="aapl", strategy=strategy, mock=True)
        trader = MockTrader(trade)

        while e.not_finished() and trader.trade.active:
            trader.follow_course(data=e.emit())

        print(eval2.json(False))
        print(trader.trade.summary.json(False))
        self.assertGreater(trader.trade.summary.gain, 0)
        trader.trade.persist("temp")


if __name__ == '__main__':
    unittest.main()
