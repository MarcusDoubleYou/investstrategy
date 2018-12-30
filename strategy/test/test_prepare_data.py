import unittest

from strategy import preparedata
from strategy.riskcalculator import StrategyEval
import pandas as pd


class RiskCalTests(unittest.TestCase):
    eval1 = StrategyEval()
    eval1.eval(2, 4, 1, 100)

    def test_prepare_data(self):
        df = pd.read_csv("resources/aapl::2018-06-01::1min.csv")
        df_prepared = preparedata.add_features(df=df)
        self.assertIsNotNone(df_prepared)

    def test_add_indicator(self):
        df = pd.read_csv("resources/aapl::2018-06-01::1min.csv")
        df_prepared = preparedata.add_features(df=df, add_all=True, drop_times=True)
        self.assertIsNotNone(df_prepared)

    def test_add_category(self):
        df = pd.read_csv("resources/aapl::2018-06-01::1min.csv")
        df_prepared = preparedata.add_features_category(df=df, volatility=True, momentum=True, trend=True)
        self.assertIsNotNone(df_prepared)

    def test_add_bollinger_band(self):
        df = pd.read_csv("resources/aapl::2018-06-01::1min.csv")
        df_prepared = preparedata.add_bollinger_band(df=df)
        self.assertIsNotNone(df_prepared)

    def test_add_moving_averages(self):
        df = pd.read_csv("resources/aapl::2018-06-01::1min.csv")
        df_prepared = preparedata.add_moving_averages(df=df)
        self.assertIsNotNone(df_prepared['sma_200'])
        self.assertIsNotNone(df_prepared['ema_20'])
        self.assertIsNotNone(df_prepared)

    # run manual to viz
    def _test_viz_donchain(self):
        import matplotlib.pyplot as plt
        df = pd.read_csv("resources/aapl::2018-06-01::1min.csv")
        df_prepared = preparedata.add_features_category(df, volatility=True)
        self.assertIsNotNone(df_prepared)
        print(df_prepared.columns)

        plt.plot(df_prepared['last'], c='black', linewidth=.4)
        plt.plot(df_prepared['volatility_dch'], c='blue', linewidth=.4)
        plt.plot(df_prepared['volatility_dcl'], c='blue', linewidth=.4)
        plt.show()

        plt.plot(df_prepared['last'], c='black', linewidth=.4)
        plt.plot(df_prepared['volatility_kch'], c='blue', linewidth=.4)
        plt.plot(df_prepared['volatility_kcl'], c='blue', linewidth=.4)
        plt.show()

    # run manual to viz
    def _test_viz_sma(self):
        import matplotlib.pyplot as plt
        df = pd.read_csv("resources/2018-12-25-ams-5min.csv")
        df_prepared = preparedata.add_moving_averages(df)
        self.assertIsNotNone(df_prepared)
        print(df_prepared.columns)

        plt.plot(df_prepared['last'], c='black', linewidth=.4)
        plt.plot(df_prepared['sma_200'], c='blue', linewidth=.4)
        plt.plot(df_prepared['ema_20'], c='green', linewidth=.4)
        plt.show()


if __name__ == '__main__':
    unittest.main()
