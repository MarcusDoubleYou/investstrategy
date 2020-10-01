import unittest

import ta
from ta import *

from strategy import preparedata
from strategy.feeder import MockEmitter
from scipy.signal import find_peaks

import numpy as np
import pandas as pd
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
        # https://stackoverflow.com/questions/31070563/find-all-local-maxima-and-minima-when-x-and-y-values-are-given-as-numpy-arrays?noredirect=1&lq=1
        x = np.array([6, 3, 5, 2, 1, 4, 9, 7, 8])
        y = np.linspace(1, len(x) + 1, num=len(x) + 1)
        # y = np.array([2, 1, 3, 5, 3, 9, 8, 10, 7])

        # sort the data in x and rearrange y accordingly
        sortId = np.argsort(x)
        x = x[sortId]
        y = y[sortId]

        # this way the x-axis corresponds to the index of x
        plt.plot(x - 1, y)
        # plt.show()
        maxm = argrelextrema(y, np.greater)  # (array([1, 3, 6]),)
        minm = argrelextrema(y, np.less)  # (array([2, 5, 7]),)

        peaks, _ = find_peaks(y)

        resistances = find_resistance(y[peaks])

        # this way the x-axis corresponds to the index of x
        plt.plot(x - 1, y)
        plt.axhline(y=9.5, xmin=0.0, xmax=1.0, color='r')
        plt.plot(peaks, y[peaks], "x")
        plt.show()


def find_peak(prices):
    x = prices
    y = np.linspace(1, len(prices) + 1, num=len(prices) + 1)


def find_resistance(peaks, resistance_level_spread=1):
    peaks_ordered = sorted(peaks, reverse=True)
    resistances = []
    skip_index = []
    for index, peak in enumerate(peaks_ordered):
        if index in skip_index:
            continue
        print(peak)
        resistance = Resistance(peak)
        lower_h = peak - resistance_level_spread
        # if another max is within the range remove it
        for jindex, j in enumerate(peaks_ordered):
            # since list is order skip higher values
            # todo might not be valid for bigger values, possibly use a range upper lower so support and resistance can be calucated in one function
            if jindex < index:
                continue
            if j >= lower_h:
                resistance.add_value(j)
                skip_index.append(jindex)
        resistances.append(resistance)
    return resistances


class Resistance:
    touch_points = []

    def __init__(self, initial_value) -> None:
        super().__init__()
        self.initial_value = initial_value
        self.touch_points.append(initial_value)

    def add_value(self, point):
        self.touch_points.append(point)

    def get_mean_resistance(self):
        return np.mean(np.array(self.touch_points))

    def get_upper_lower_limit(self):
        pass

    def get_touch_points(self):
        return len(self.touch_points)

# simple way of finding support lines/ area needs to be touched at least three times
# concept of similarity
# re-frame the idea of pattern matching
# find a few successfull moves and do similarity matching