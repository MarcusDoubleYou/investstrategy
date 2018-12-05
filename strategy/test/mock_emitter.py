import pandas as pd

import numpy as np


def rand_df(self):
    return pd.DataFrame(np.random.randint(low=0, high=10, size=(5, 5)),
                        columns=['price', 'vl', 'open', 'close', 'hi'])


class Emitter:
    _data = None
    _index = 0

    def __init__(self, index=0, len=10, data=None) -> None:
        self._index = index
        if data is None:
            self._data = pd.DataFrame(np.random.randint(low=1, high=10, size=(len, 6)),
                                      columns=['price', 'vl', 'open', 'close', 'hi', 'last'])
        else:
            self._data = data

        super().__init__()

    def emit(self):
        self._index = self._index + 1
        return self._data[self._index - 1:self._index]

    def not_finished(self):
        return self._index < self._data.shape[0]

# sample use
# e = Emiiter()
# print(e.not_finished())
# while e.not_finished():
#     print(e.emit())
