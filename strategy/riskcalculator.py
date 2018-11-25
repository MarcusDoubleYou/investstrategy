import json
import math

from strategy.strategy_eval import BaseStrategy


class StrategyException(Exception):

    def __init__(self, *args: object, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)


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
    rio = 0
    rio_per = ""
    # 1/2 => means you rewards is double your risk or differently willing to risk $1 to win $2
    risk_reward_ratio = 0
    risk_reward_ratio_per = ""
    commission = 10.0
    percentage_loss = 0.0
    percentage_win = 0.0

    #  value for long add different type if bull or bear
    def _calc(self):
        if self.entry >= self.target:
            raise AssertionError("entry cannot be higher than target")
        if self.target <= self.stop:
            raise AssertionError("stop cannot be higher than target")
        if self.entry < 0.0 or self.target < 0.0 or self.quantity < 0.0:
            raise AssertionError("values cannot be less or equal to 0.0")

        self.investment = self.quantity * self.entry + self.commission
        self.win = (self.quantity * self.target) - self.investment
        self.loss = (self.quantity * self.stop) - self.investment
        self.risk_reward_ratio = self.win / self.loss * -1
        self.risk_reward_ratio_per = "1/" + str(self.risk_reward_ratio)
        self.rio = (((self.quantity * self.target) - self.investment) / self.investment)  # * -1
        self.rio_per = str(self.rio * 100) + "%"
        self.loss_per_stock_per = (self.stop - self.entry) / self.entry
        self.loss_per_stock = self.stop - self.entry
        self.win_per_stock_per = (self.target - self.entry) / self.entry
        self.win_per_stock = self.target - self.entry

    def eval(self, entry, target, stop, quantity, commission=10):
        self.quantity = quantity
        self.entry = entry
        self.target = target
        self.stop = stop
        self._calc()
        self.commission = commission
        return self

    def eval_strategy(self, strategy: BaseStrategy):
        self.eval(strategy.entry, strategy.target, strategy.stop, strategy.quantity)
        return self

    def ratio_worth(self, risk_reward_ratio=2):
        return self.risk_reward_ratio > risk_reward_ratio

    def positive_return(self, raise_error=False):
        positive = not (self.rio < 0 or self.risk_reward_ratio < 0)
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

        self.entry = entry
        self.target = target
        self.quantity = math.floor((investment - self.commission) / self.entry)
        loss_per_share = (acceptable_loss / self.quantity)
        self.stop = self.entry - loss_per_share
        self._calc()
        return self

    def json(self, log=True):
        j = json.dumps(self.__dict__)
        if log:
            print(j)
        return j

# def shares_to_buy(entry, target, stop, exceptable_total_loss):
#     if entry >= target:
#         raise AssertionError
#     if target <= stop:
#         raise AssertionError
#     loss_per_stock = entry - stop
#     shares = math.ceil(exceptable_total_loss / loss_per_stock)
#     win = shares * target - shares * entry
#     print_trade_stats(win, loss_per_stock * shares, shares, shares * entry)
#
#
# def shares_to_buy_per(entry, target, stop, investment, loss_percent):
#     if loss_percent >= 1.0:
#         loss_percent = loss_percent / 100
#     loss = (investment * loss_percent)
#     shares_to_buy(entry, target, stop, loss)
#
#
# def print_trade_stats(possible_gain, possilbe_loss, shares, investment):
#     print("------------START-------------")
#     print("shares to buy ", shares)
#     print("win abs +", round(possible_gain, 3))
#     print("loss abs -", round(possilbe_loss, 3))
#     print("ROI win +", round((possible_gain / investment), 3))
#     print("ROI loss -", round((possilbe_loss / investment), 3))
#     print("win loss relationship ", round((possible_gain / possilbe_loss), 3))
#     print("investment ", investment)
#     print("------------FINISH------------")


# shares_to_buy(3.78, 4.0, 2.0, 100)
#
# shares_to_buy(3.0, 4.0, 2.0, 100)
#
# shares_to_buy(3.0, 4.0, 2.85, 100)
#
# shares_to_buy(3.0, 3.25, 2.85, 100)
# #
# # shares_to_buy_per(3.0, 4.0, 2.85, 1000, 0.01)
#
# shares_to_buy_per(5.05, 5.48, 4.60, 1000, 10)

# class Trade:
#     symbol = ""
#     entry = 0.0
#     target = 0.0
#     stop = 0.0
#     shares = 0.0
#     loss = 0.0
#     investment = shares * entry
#
#     def __init__(self, entry, target, stop, shares, loss) -> None:
#         super().__init__()
#         entry = entry
#         target = target
#         stop = stop
#         shares = shares
#         loss = loss
#
#     def print_nice(self):
#         shares_to_buy_per(entry, target, stop, stop)
#
#     def __str__(self) -> str:
#         return super().__str__()
#
#
# trade = Trade(5.05, 5.48, 4.60, 1000, 10)
# trade.print_nice()
