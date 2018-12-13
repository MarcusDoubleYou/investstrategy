import unittest

from strategy.riskcalculator import StrategyEval


class RiskCalTests(unittest.TestCase):
    eval1 = StrategyEval()
    eval1.eval(2, 4, 1, 100)

    def test_cal_risk(self):
        self.assertIsNotNone(self.eval1.json())

    def test_2(self):
        eval2 = StrategyEval()
        eval2.eval(1, 3.5, 0.8, 5000)
        self.assertIsNotNone(eval2.json())
        self.assertEqual(round(eval2.roi, 1), 2.5)

    def test_risk(self):
        #  sample from https://www.investopedia.com/terms/r/riskrewardratio.asp
        eval2 = StrategyEval()
        eval2.eval(20, 30, 15, 100)
        self.assertIsNotNone(eval2.json())
        self.assertEqual(round(eval2.risk_reward_ratio), 2)
        self.assertEqual(eval2.loss, -510.0)
        self.assertEqual(eval2.win, 990.0)
        self.assertEqual(eval2.loss_per_stock, -5)
        self.assertEqual(eval2.loss_per_stock_per, -0.25)
        self.assertFalse(eval2.ratio_worth())

    def test_risk_target_percent(self):
        #  sample from https://www.investopedia.com/terms/r/riskrewardratio.asp
        eval2 = StrategyEval()
        eval2.eval(20.0, "50%", 15, 100)
        self.assertIsNotNone(eval2.json())
        self.assertEqual(round(eval2.risk_reward_ratio), 2)
        self.assertEqual(eval2.loss, -510.0)
        self.assertEqual(eval2.win, 990.0)
        self.assertEqual(eval2.loss_per_stock, -5)
        self.assertEqual(eval2.loss_per_stock_per, -0.25)
        self.assertFalse(eval2.ratio_worth())

    def test_risk_strings(self):
        eval2 = StrategyEval()
        eval2.eval("20.0", "50%", "15", 100.5)
        self.assertIsNotNone(eval2.json())
        self.assertEqual(round(eval2.risk_reward_ratio), 2)
        self.assertEqual(eval2.loss, -510.0)
        self.assertEqual(eval2.win, 990.0)
        self.assertEqual(eval2.loss_per_stock, -5)
        self.assertEqual(eval2.loss_per_stock_per, -0.25)
        self.assertFalse(eval2.ratio_worth())

    def test_risk_investment(self):
        #  sample from https://www.investopedia.com/terms/r/riskrewardratio.asp
        eval2 = StrategyEval()
        eval2.eval_with_loss_of_investment(20, 30, 2000, 500)
        self.assertIsNotNone(eval2.json())
        self.assertEqual(round(eval2.risk_reward_ratio), 2)
        self.assertEqual(round(eval2.loss), -510.0)
        self.assertEqual(eval2.win, 980.0)

    def test_risk_investment_percent(self):
        eval2 = StrategyEval()
        eval2.eval_with_loss_of_investment(20, 30, 2000, acceptable_loss="25%")
        self.assertIsNotNone(eval2.json())
        self.assertEqual(round(eval2.risk_reward_ratio), 2)
        self.assertEqual(round(eval2.loss), -510.0)
        self.assertEqual(eval2.win, 980.0)

    def test_risk_investment_commission(self):
        eval2 = StrategyEval()
        eval2.eval_with_loss_of_investment(20, 30, 2000, "25%", commission=20)
        self.assertIsNotNone(eval2.json())
        self.assertEqual(round(eval2.risk_reward_ratio), 2)
        self.assertEqual(round(eval2.loss), -520.0)
        self.assertEqual(eval2.win, 970.0)
        self.assertEqual(eval2.commission, 20.0)

    def test_risk_percentage_target(self):
        eval2 = StrategyEval()
        eval2.eval_with_loss_of_investment(20, "50%", 2000, "25%", commission=20)
        self.assertIsNotNone(eval2.json())
        self.assertEqual(round(eval2.risk_reward_ratio), 2)
        self.assertEqual(round(eval2.loss, 1), -520.0)
        self.assertEqual(eval2.win, 970.0)
        self.assertEqual(eval2.commission, 20.0)

    def test_create_strategy_from_risk(self):
        eval2 = StrategyEval()
        eval2.eval_with_loss_of_investment(10, 30, 2000, "25%", commission=20)
        strategy = eval2.create_trade_strategy()
        self.assertIsNotNone(strategy)
        self.assertIsNotNone(strategy.buy_trigger)
        self.assertIsNotNone(strategy.sell_order)
        self.assertIsNotNone(strategy.stop_trigger)
        self.assertIsNotNone(strategy.quantity)
        self.assertIsNotNone(strategy.commission)
        self.assertEqual(20, strategy.commission)

    def test_create_strategy_from_risk_2(self):
        eval2 = StrategyEval()
        eval2.eval_with_loss_of_investment(7.75, "4.5%", 1000, "10%", commission=10)
        strategy = eval2.create_trade_strategy()
        print(eval2.json())
        self.assertIsNotNone(strategy)
        self.assertIsNotNone(strategy.buy_trigger)
        self.assertIsNotNone(strategy.sell_order)
        self.assertIsNotNone(strategy.stop_trigger)
        self.assertIsNotNone(strategy.quantity)
        self.assertIsNotNone(strategy.commission)


if __name__ == '__main__':
    unittest.main()

#
# def print_trade_stats(possible_gain, possilbe_loss, shares, investment):
#     print("------------START-------------")
#     print("shares to buy ", shares)
#     print("win abs +", round(possible_gain, 3))
#     print("loss abs -", round(possilbe_loss, 3))
#     print("ROI win +", round((possible_gain / investment), 3))
#     print("ROI loss -", round((possilbe_loss / investment), 3))
#     print("win loss relationship ", round((possible_gain / possilbe_loss), 3))
#     print("investment ", investment)
#     print("------------FINISH------------")
