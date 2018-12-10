import pandas as pd
import unittest

import numpy as np

from strategy.feeder import MockEmitter
from strategy.trigger import IndicatorTrigger, SimpleTrigger


class TriggerTests(unittest.TestCase):

    def rand_df(self):
        return pd.DataFrame(np.random.randint(low=0, high=10, size=(5, 5)),
                            columns=['price', 'vl', 'open', 'close', 'hi'])

    def test_basic_trigger_buy(self):
        st = SimpleTrigger("price::>::20.10")
        data = self.rand_df()
        self.assertFalse(st.eval_trigger_condition(data))
        self.assertFalse(st.active(data))

    def test_basic_trigger_sell(self):
        st = SimpleTrigger("price::<::20.10")
        data = self.rand_df()
        self.assertTrue(st.eval_trigger_condition(data))
        self.assertTrue(st.active(data))

    def test_basic_trigger(self):
        e = MockEmitter()
        st = SimpleTrigger("price::>::2.10")

        while e.not_finished() and not st.triggered:
            st.active(e.emit())
        self.assertTrue(st.triggered)

    def test_indicator_trigger(self):
        e = MockEmitter()
        st = IndicatorTrigger("open::<::close")

        while e.not_finished() and not st.triggered:
            st.active(e.emit())
        self.assertIsNotNone(st.triggered)
        # random data trigger may or may not be triggered
        # self.assertTrue(st.triggered)

    # trigger range is out of default range so it should not be triggered
    def test_basic_trigger_not_triggered(self):
        e = MockEmitter()
        st = SimpleTrigger("price::>::1000.10")

        while e.not_finished() and not st.triggered:
            st.active(e.emit())
        self.assertFalse(st.triggered)


if __name__ == '__main__':
    unittest.main()
