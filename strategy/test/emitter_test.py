import unittest

from strategy.feeder import MockEmitter


class EmitterTests(unittest.TestCase):

    def test_cal_risk(self):
        emitter = MockEmitter()
        while emitter.not_finished():
            self.assertIsNotNone(emitter.emit())
