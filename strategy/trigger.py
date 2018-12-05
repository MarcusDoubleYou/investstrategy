'''

indicates if trade order should be executed

base class
takes a data => feeder
'''


class TradeTrigger:
    buy = True
    triggered = False
    trigger_type = None
    trigger_description = ""

    def __init__(self, buy=True) -> None:
        super().__init__()
        self.buy = buy

    # def wait_for_trigger(self, sleep=5):
    #     while not self.trigger:
    #         pass

    def eval_trigger_condition(self, data):
        pass

    def active(self, data):
        if self.triggered:
            raise Exception("trigger has been activated")
        if self.eval_trigger_condition(data):
            self.triggered = True
        return self.triggered

    def to_json(self):
        pass


'''
description => df_variable::comparator::target_value::trigger_type
'''


def trigger_parts(trigger_description):
    parts = trigger_description.split("::")
    if parts.__len__() == 3:
        return parts[0], parts[1], parts[2]
    elif parts.__len__() == 4:
        return parts[0], parts[1], parts[2], parts[3]
    else:
        raise NotImplementedError("trigger description cannot be parsed")


def get_trigger_type(trigger_description):
    _df_variable, _comparator, _target_value, _trigger_type = trigger_parts(trigger_description)
    if _target_value is None:
        return SimpleTrigger(trigger_description)
    elif _trigger_type == "INDICATOR":
        return IndicatorTrigger(trigger_description)


class SimpleTrigger(TradeTrigger):
    _df_variable = "price"
    _comparator = ">"
    _target_value = 0.0

    def __init__(self, trigger_description, buy=True) -> None:
        super().__init__(buy=buy)
        self.trigger_type = "SIMPLE"
        self.trigger_description = trigger_description
        self._df_variable, self._comparator, self._target_value = trigger_parts(trigger_description)

    def eval_trigger_condition(self, data):
        if self._comparator == ">":
            return data[self._df_variable].values[-1] >= float(self._target_value)
        elif self._comparator == "<":
            return data[self._df_variable].values[-1] <= float(self._target_value)
        else:
            # better exc
            raise Exception


class IndicatorTrigger(TradeTrigger):
    _df_variable = ""
    _comparator = ""
    _df_target_variable = ""

    def __init__(self, trigger_description, buy=True) -> None:
        super().__init__(buy=buy)
        self.trigger_type = "INDICATOR"
        self.trigger_description = trigger_description
        self._df_variable, self._comparator, self._df_target_variable = trigger_parts(trigger_description)

    def eval_trigger_condition(self, data):
        if self._comparator == ">":
            return data[self._df_variable].values[-1] >= data[self._df_target_variable].values[-1]
        elif self._comparator == "<":
            return data[self._df_variable].values[-1] <= data[self._df_target_variable].values[-1]
        else:
            # better exc
            raise Exception("trigger condition could not be evaluated")
