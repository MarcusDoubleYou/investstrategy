import unittest
import pandas as pd

from strategy.feeder import MockEmitter


class EmitterTests(unittest.TestCase):

    def test_emitter(self):
        emitter = MockEmitter()
        while emitter.not_finished():
            self.assertIsNotNone(emitter.emit())

    def test_emitter_loaded_data(self):
        data = pd.read_csv("temp/aapl::2018-06-01::1min.csv")
        emitter = MockEmitter(data=data)
        while emitter.not_finished():
            self.assertIsNotNone(emitter.emit())
            # print(emitter.tail())
