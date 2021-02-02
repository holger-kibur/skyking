import math

class ConfigField(object):
    def __init__(self, default):
        self.set_value(default)
        if not self.value:
            raise ValueError("Field default isn't valid!")

    def from_raw(self, raw):
        raise NotImplementedError()

    def to_raw(self):
        raise NotImplementedError()

    def set_value(self, val):
        if self.validate(val):
            self.value = val

    def get_value(self):
        return self.value

    def validate(self, val):
        raise NotImplementedError()

class IntegerField(ConfigField):
    def __init__(self, default, min_=-math.inf, max_=math.inf):
        super().__init__(default)
        self.min = min_
        self.max = max_

    def from_raw(self, raw):
        self.value = int(raw)

    def to_raw(self):
        return str(self.value)

    def validate(self, val):
        try:
            val = int(val)
        except ValueError:
            return False
        return self.min <= val <= self.max

class FloatField(ConfigField):
    def __init__(self, default, min_=-math.inf, max_=math.inf):
        super().__init__(default)
        self.min = min_
        self.max = max_

    def from_raw(self, raw):
        self.value = float(raw)

    def to_raw(self):
        return str(self.value)

    def validate(self, val):
        try:
            val = float(val)
        except ValueError:
            return False
        return self.min <= val <= self.max

class StaticConfiguration(object):
    def __init__(self, config_owner, **kwargs):
        self.config_owner = config_owner
        self.fields = kwargs