'''
 when ever it receive an updated based on the state of the trade it evaluates and makes a decision
 responsible for state management
'''
import json

from strategy.domain import Trade, TradeSummary
from strategy.trigger import SimpleTrigger
from strategy.utils import TradeState, ProjectTime, remove_key


class MarketDataFeederType:
    REAL_TIME = "REAL_TIME"
    MOCK_DATA = "MOCK_DATA"
    REAL_DATA_REPLAY = "REAL_DATA_REPLAY"


# py 3.7
# @dataclass
class TraderConfig:
    """
    needs to be merged with trader class or maybe become part of the trader class
    configures how data will be pulled and what kind of data will be used
    """
    symbol: str = "mock"
    feeder_type: str = MarketDataFeederType.MOCK_DATA
    env: str = "test"
    # wait time between trader pulling the feeder
    market_data_pull_interval_sec: int = 5
    # timeintervall of market data (1min, 5min .. .)
    market_data_interval: str = "1min"
    trader_address: str = "localhost"
    startdate_days_ago: int = 1
    enddate_days_ago: int = 0

    def __init__(self,
                 symbol: str = "mock",
                 feeder_type: str = MarketDataFeederType.MOCK_DATA,
                 env: str = "test",
                 market_data_pull_interval_sec: int = 5,
                 market_data_interval: str = "1min",
                 trader_address: str = "localhost",
                 startdate_days_ago: int = 1,
                 enddate_days_ago: int = 0
                 ) -> None:
        super().__init__()
        self.env = env
        self.enddate_days_ago = enddate_days_ago
        self.startdate_days_ago = startdate_days_ago
        self.trader_address = trader_address
        self.market_data_interval = market_data_interval
        self.market_data_pull_interval_sec = market_data_pull_interval_sec
        self.feeder_type = feeder_type
        self.symbol = symbol

    def get_feeder(self):
        """ subclass overwrites in order integrate with remote data source. see trader-app project  """
        pass

    def to_json(self):
        # py 3.7
        #     return asdict(self)
        return self.__dict__

    def from_json(self):
        pass


def default_config():
    return TraderConfig()


def from_dict(config_dict):
    if config_dict is None:
        return None
    return TraderConfig(env=config_dict.get('env'),
                        symbol=config_dict.get('symbol'),
                        feeder_type=config_dict.get('feeder_type'),
                        market_data_pull_interval_sec=config_dict.get('market_data_pull_interval_sec'),
                        market_data_interval=config_dict.get('market_data_interval'),
                        trader_address=config_dict.get('trader_address'),
                        startdate_days_ago=config_dict.get('startdate_days_ago'),
                        enddate_days_ago=config_dict.get('enddate_days_ago')
                        )


class Trader:
    """
    Basic Trader
    manages state of trade
    data feeder

    to integrate with different broker just subclass trader and overwrite/ implement data
    """

    trade: Trade = None
    config: TraderConfig = None
    emitter = None
    data = None

    def __init__(self, trade: Trade, config: TraderConfig = None) -> None:
        super().__init__()
        self.trade = trade
        self.trade.active = True
        if config is None:
            self.config = default_config()
        else:
            self.config = config
        self.config.symbol = trade.symbol

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
        _dict = remove_key(self.__dict__, "data")
        _dict = remove_key(_dict, "emitter")
        return json.dumps(_dict, default=lambda o: o.to_json())


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
    """
    check out the trader project
    """
    pass


class TrainableAgent(Trader):
    """
    target is gain => needs to be constantly updated
    forcast stock price based on time series prediction and then run simulation to find optimum
    """
    pass
