'''
 when ever it receive an updated based on the state of the trade it evaluates and makes a decision
 responsible for state management
'''
import json

from strategy.domain import Trade, TradeSummary
from strategy.trigger import SimpleTrigger
from strategy.utils import TradeState, ProjectTime


class Trader:
    """
    Basic Trader
    manages state of trade
    data feeder

    to integrate with different broker just subclass trader and overwrite/ implement data
    """

    trade: Trade = None
    data = None
    emitter = None

    def __init__(self, trade) -> None:
        super().__init__()
        self.trade = trade
        self.trade.active = True

    def buy(self):
        # TODO infer trigger type based on description
        t = SimpleTrigger(self.trade.strategy.buy_trigger)
        if t.eval_trigger_condition(self.data):
            self.place_order(buy=True)
        pass

    def sell(self):
        t = SimpleTrigger(self.trade.strategy.sell_trigger)
        # if type(self.trade.strategy.stop_trigger) == float:
        stop = SimpleTrigger(self.trade.strategy.stop_trigger)
        if t.eval_trigger_condition(self.data) or stop.eval_trigger_condition(self.data):
            self.place_order(buy=False)
        pass

    def follow_course(self, **kwargs):
        """
        entry point for receiving new data and acting based on state
        todo add preprocessor for data e.g. add moving averages
        :param kwargs:
        :return:
        """
        if kwargs.keys().__contains__('data'):
            self.data = kwargs['data']

        if self.data is None:
            print("no data present")
            return

        if self.trade.state == TradeState.WATCHING:
            self.buy()
        elif self.trade.state == TradeState.HOLDING:
            self.sell()
        elif self.trade.state == TradeState.PLACED_BUY_ORDER:
            self.waiting_to_fulfil_order()
        elif self.trade.state == TradeState.PLACED_SELL_ORDER:
            self.waiting_to_fulfil_order()
        elif self.trade.state == TradeState.FINISHED:
            self.finish()
        pass

    def change_state(self, new_state, action=""):
        message = ProjectTime().string_time() + "STATE CHANGE: symbol: " + self.trade.symbol + \
                  " Old state: " + self.trade.state + \
                  " New state: " + new_state + " trigger_action: " + action
        self.trade.state = new_state
        self.trade.state_history.append(new_state)
        print(message)
        pass

    def start(self):
        pass

    def pause(self):
        pass

    def finish(self):
        self.trade.active = False
        # todo get trade summary from broker and use this instead
        print("WARNING no summary is produced for real trades.")
        pass

    def place_order(self, buy=False):
        d = ProjectTime().string_time()
        if buy:
            print(d + " ACTION: Placed Buy order ", self.trade.symbol)
        else:
            print(d + " ACTION: Placed sell order ", self.trade.symbol)
        pass

    def waiting_to_fulfil_order(self):
        pass

    def update_strategy(self):
        pass

    def to_json(self):
        return json.dumps(self.__dict__, default=lambda o: o.to_json())


class MockTrader(Trader):
    """
    Mock trader => all transaction are successful immediately

    """

    def place_order(self, buy=False):
        super().place_order(buy)
        if buy:
            self.change_state(TradeState.PLACED_BUY_ORDER)
        else:
            self.change_state(TradeState.PLACED_SELL_ORDER)

    def waiting_to_fulfil_order(self):
        super().waiting_to_fulfil_order()
        if self.trade.state == TradeState.PLACED_BUY_ORDER:
            print("order has been placed waiting to be fulfilled ")
            self.change_state(TradeState.HOLDING)
            self.trade.buy_price = float(self.data.tail(1)['last'].values[0])
        elif self.trade.state == TradeState.PLACED_SELL_ORDER:
            self.finish()
            self.change_state(TradeState.FINISHED)
            # self.summary.finished(self.course)
            # self.summary.json()

    def finish(self):
        super().finish()
        self.trade.finish(self.data.tail(1)['last'].values[0])
        self.trade.persist(path="temp")


class AgentTrader(Trader):
    pass
