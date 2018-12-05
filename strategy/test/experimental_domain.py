class TargetValue:

    def __init__(self, value=None, value_type="SIMPLE", data=None, target_name=None) -> None:
        super().__init__()
        self.targetName = target_name
        self.data = data
        self.value_type = value_type
        self.value = value

    def v(self):
        if self.value_type == "SIMPLE":
            return self.value
        elif self.value_type == "FROM_DF":
            return self.data[self.targetName]
        else:
            raise NotImplementedError("value type unknown")


t1 = TargetValue(1.1)
print(t1.v())
