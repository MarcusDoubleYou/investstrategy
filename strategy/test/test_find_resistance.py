import unittest

import ta
from ta import *

from strategy import preparedata
from strategy.feeder import MockEmitter
from scipy.signal import find_peaks

import numpy as np
import matplotlib.pyplot as plt

import numpy as np
from scipy.signal import argrelextrema
import pandas as pd
import matplotlib.pyplot as plt


class TestResistance(unittest.TestCase):

    def test_cal_resistance(self):
        data = pd.read_csv("resources/ugaz-1min.csv")
        data = preparedata.add_macd(data)
        # data = data[100:300]
        data = data[-100:]
        x = np.arange(100)

    # https://stackoverflow.com/questions/31070563/find-all-local-maxima-and-minima-when-x-and-y-values-are-given-as-numpy-arrays?noredirect=1&lq=1

    def test_cal_local_min_max(self):
        # https://stackoverflow.com/questions/31070563/find-all-local-maxima-and-minima-when-x-and-y-values-are-given-as-numpy-arrays?noredirect=1&lq=1
        # x = np.array([6, 3, 5, 2, 1, 4, 9, 7, 8])
        # y = np.linspace(1, len(x) + 1, num=len(x) + 1)
        y = np.array([2, 1, 3, 5, 3, 9, 8, 10, 7])
        x = np.linspace(1, len(y), num=len(y))

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

    def test_find_resistance(self):
        data = pd.read_csv("resources/ugaz-1min.csv")
        data = data[-100:]
        peaks = find_peak_values(data['last'].values)
        print(peaks)

    def test_show_resistance(self):
        data = pd.read_csv("resources/ugaz-1min.csv")
        y = data[-100:]
        y = y['last'].values
        peaks = find_peak_values(y)
        resistances = find_resistance(y[peaks], 0.05)

        x = np.linspace(1, len(y), num=len(y))
        plt.plot(x - 1, y)
        for r in resistances:
            plt.axhline(y=r.mean(), xmin=0.0, xmax=1.0, color='r')
        plt.plot(peaks, y[peaks], "x")
        plt.show()
        print(peaks)


def find_peak_values(prices):
    y = prices
    x = np.linspace(1, len(prices), num=len(prices))

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
    return peaks


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
        self.touch_points = [initial_value]

    def add_value(self, point):
        self.touch_points.append(point)

    def mean(self):
        return np.mean(np.array(self.touch_points))

    def upper_lower_limit(self):
        pass

    def touch_points(self):
        return len(self.touch_points)

# simple way of finding support lines/ area needs to be touched at least three times
# concept of similarity
# re-frame the idea of pattern matching
# find a few successfull moves and do similarity matching
