import json
import math

from strategy.domain import TradeStrategy, StrategyName
from strategy.strategies import BaseStrategy


class StrategyException(Exception):

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)


'''
TODO evaluates and creates trade strategies
static class
currently only works for bull stocks
'''


class StrategyEval:
    entry = 0
    target = 0
    stop = 0
    quantity = 0
    investment = 0
    win = 0
    loss = 0
    #  RIO, percentage you will get back per share
    #  e.g. buy 1 sell 1.25 => RIO of 25% or $0.25 per share invested
    roi = 0
    roi_per = ""
    # 1/2 => means you rewards is double your risk or differently willing to risk $1 to win $2
    risk_reward_ratio = 0
    risk_reward_ratio_per = ""
    commission = 10.0
    percentage_loss = 0.0
    percentage_win = 0.0
    loss_per_stock_per = 0.0
    loss_per_stock = 0.0
    win_per_stock_per = 0.0
    win_per_stock = 0.0

    #  value for long add different type if bull or bear
    def _calc(self):
        if self.entry >= self.target:
            raise AssertionError("entry cannot be higher than target")
        if self.target <= self.stop:
            raise AssertionError("stop cannot be higher than target")
        if self.entry < 0.0 or self.target < 0.0 or self.quantity < 0.0:
            raise AssertionError("values cannot be less or equal to 0.0")

        self.stop = round(self.stop, 4)
        self.investment = self.quantity * self.entry + self.commission
        self.win = round((self.quantity * self.target) - self.investment, 4)
        self.loss = round((self.quantity * self.stop) - self.investment, 4)
        self.risk_reward_ratio = round(self.win / self.loss * -1, 4)
        self.risk_reward_ratio_per = "1/" + str(self.risk_reward_ratio)
        self.roi = (((self.quantity * self.target) - self.investment) / self.investment)  # * -1
        self.roi_per = str(round(self.roi * 100, 4)) + "%"
        self.loss_per_stock_per = round((self.stop - self.entry) / self.entry, 4)
        self.loss_per_stock = round(self.stop - self.entry, 4)
        self.win_per_stock_per = round((self.target - self.entry) / self.entry, 4)
        self.win_per_stock = round(self.target - self.entry, 4)

    def eval(self, entry, target, stop, quantity, commission=10):
        self.quantity = int(quantity)
        self.entry = float(entry)
        # target can be given as percentage gain
        if type(target) is str:
            target = (float(str(target).replace("%", "")) / 100) * self.entry + self.entry
        self.target = float(target)
        self.stop = float(stop)
        self._calc()
        self.commission = float(commission)
        if not self.stop < self.entry < self.target:
            raise Exception("strategy has invalid values verify entry, target and stop")
        return self

    def ratio_worth(self, risk_reward_ratio=2):
        return self.risk_reward_ratio > risk_reward_ratio

    def positive_return(self, raise_error=False):
        positive = not (self.roi < 0 or self.risk_reward_ratio < 0)
        if raise_error and not positive:
            raise StrategyException("Negative return. Trade is not worth it!")
        return positive

    def eval_with_loss_of_investment(self, entry, target, investment, acceptable_loss, commission=10):
        self.commission = commission
        if type(acceptable_loss) is str:
            excepted_loss_percent = str(acceptable_loss).replace("%", "")
            try:
                excepted_loss_percent = int(excepted_loss_percent) / 100
            except TypeError:
                pass
            acceptable_loss = investment * excepted_loss_percent

        # target can be given as percentage gain
        if type(target) is str:
            target = (float(str(target).replace("%", "")) / 100) * entry + entry

        self.entry = entry
        self.target = target
        self.quantity = math.floor((investment - self.commission) / self.entry)
        loss_per_share = (acceptable_loss / self.quantity)
        self.stop = self.entry - loss_per_share
        self._calc()
        return self

    def create_trade_strategy(self, strategy_name=StrategyName.DAY_BULL):
        return TradeStrategy(buy_trigger="last::>::" + str(self.entry),
                             sell_trigger="last::>::" + str(self.target),
                             stop_trigger="last::<::" + str(self.stop),
                             quantity=self.quantity,
                             name=strategy_name,
                             commission=self.commission,
                             description="Created by strategy evaluator.")

    def json(self, log=True):
        j = json.dumps(self.__dict__)
        if log:
            print(j)
        return j

    def to_json(self):
        return self.__dict__

    @DeprecationWarning
    def eval_strategy(self, strategy: BaseStrategy):
        # todo implemented against strategy
        # only simple strategy would work
        self.eval(strategy.entry, strategy.target, strategy.stop, strategy.quantity)
        return self
