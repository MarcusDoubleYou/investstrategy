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
        self.assertEqual(round(eval2.rio, 1), 2.5)

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

    def test_risk_investment(self):
        #  sample from https://www.investopedia.com/terms/r/riskrewardratio.asp
        eval2 = StrategyEval()
        eval2.eval_with_loss_of_investment(20, 30, 2000, 500)
        self.assertIsNotNone(eval2.json())
        self.assertEqual(round(eval2.risk_reward_ratio), 2)
        self.assertEqual(eval2.loss, -510.0)
        self.assertEqual(eval2.win, 980.0)

    def test_risk_investment_percent(self):
        eval2 = StrategyEval()
        eval2.eval_with_loss_of_investment(20, 30, 2000, acceptable_loss="25%")
        self.assertIsNotNone(eval2.json())
        self.assertEqual(round(eval2.risk_reward_ratio), 2)
        self.assertEqual(eval2.loss, -510.0)
        self.assertEqual(eval2.win, 980.0)

    def test_risk_investment_commission(self):
        eval2 = StrategyEval()
        eval2.eval_with_loss_of_investment(20, 30, 2000, "25%", commission=20)
        self.assertIsNotNone(eval2.json())
        self.assertEqual(round(eval2.risk_reward_ratio), 2)
        self.assertEqual(eval2.loss, -520.0)
        self.assertEqual(eval2.win, 970.0)
        self.assertEqual(eval2.commission, 20.0)


if __name__ == '__main__':
    unittest.main()


def sample():
    eval2 = StrategyEval()
    eval2.commission = 20
    eval2 = eval2.eval_with_loss_of_investment(1.35, 1.43, 1000, "2%")
    eval2.json()

# sample()
