import pandas as pd
import numpy as np


def rand_df():
    return pd.DataFrame(np.random.randint(low=0, high=10, size=(5, 5)),
                        columns=['price', 'vl', 'open', 'close', 'hi'])


class Emitter:
    _data: pd.DataFrame = None
    _index = 0

    def __init__(self, data=None) -> None:
        self._data = data
        super().__init__()

    def _pull_for_updates(self):
        pass

    def emit(self, full=True):
        self._pull_for_updates()
        if full:
            return self._data
        else:
            return self._data[self._index - 1:self._index]

    def not_finished(self):
        pass

    def tail(self):
        return self._data.tail(1)


class MockEmitter(Emitter):
    _index = 0
    _mock_data = None

    def __init__(self, data=None, index=0, len=20) -> None:
        """

        :param data: gets assigned to mock holds entire data
        :param index: start index
        :param len:
        """
        if data is None:
            self._data = pd.DataFrame(np.random.randint(low=1, high=10, size=(len, 6)),
                                      columns=['price', 'vl', 'open', 'close', 'hi', 'last'])
        else:
            self._data = data

        # assign mock data to data and set data to beginning
        self._mock_data = self._data
        self._data = self._mock_data.iloc[:1]

    def _pull_for_updates(self):
        super()._pull_for_updates()
        self._index = self._index + 1
        # pull from mock data
        self._data = self._mock_data.iloc[:self._index]

    def not_finished(self):
        return self._index < self._mock_data.shape[0]


class BrokerEmitter(Emitter):

    def _pull_for_updates(self):
        super()._pull_for_updates()
        # self.data = remote_call_returns_data
