import unittest

import ta
from ta import *

from strategy import preparedata
from strategy.feeder import MockEmitter

import numpy as np
import matplotlib.pyplot as plt

import numpy as np
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt


class EtfsTests(unittest.TestCase):

    def test_emitter_loaded_data(self):
        data = pd.read_csv("resources/aapl::2018-06-01::1min.csv")
        emitter = MockEmitter(data=data)
        while emitter.not_finished():
            self.assertIsNotNone(emitter.emit())
            # print(emitter.tail())

    def test_add_rsi_macd(self):
        data = pd.read_csv("resources/ugaz-1min.csv")
        data = preparedata.add_macd(data)
        # data = data[100:300]
        data = data[-100:]
        x = np.arange(100)

        plt.subplot(3, 1, 1)
        plt.plot(data['last'], linewidth=.70, c="black")
        plt.title('price')

        plt.subplot(3, 1, 2)
        plt.bar(x, data['macd_diff'], alpha=0.3)
        plt.plot(x, data['macd_signal'], linewidth=.70, c="orange")
        plt.plot(x, data['macd'], linewidth=.70, c="blue")
        plt.xlabel('mac d')

        plt.subplot(3, 1, 3)
        plt.plot(data['rsi'], linewidth=.70, c="black")
        plt.title('rsi')

        plt.show()

    def test_cal_resistance(self):
        data = pd.read_csv("resources/ugaz-1min.csv")
        data = preparedata.add_macd(data)
        # data = data[100:300]
        data = data[-100:]
        x = np.arange(100)

    def test_cal_local_min_max(self):
        x = np.array([6, 3, 5, 2, 1, 4, 9, 7, 8])
        y = np.array([2, 1, 3, 5, 3, 9, 8, 10, 7])

        # sort the data in x and rearrange y accordingly
        sortId = np.argsort(x)
        x = x[sortId]
        y = y[sortId]

        # this way the x-axis corresponds to the index of x
        plt.plot(x - 1, y)
        plt.show()
        maxm = argrelextrema(y, np.greater)  # (array([1, 3, 6]),)
        minm = argrelextrema(y, np.less)  # (array([2, 5, 7]),)

        from scipy.signal import find_peaks

        peaks, _ = find_peaks(y)

        # this way the x-axis corresponds to the index of x
        plt.plot(x - 1, y)
        plt.plot(peaks, y[peaks], "x")
        plt.show()

# simple way of finding support lines/ area needs to be touched at least three times
# concept of similarity
# re-frame the idea of pattern matching
# find a few successfull moves and do similarity matching
