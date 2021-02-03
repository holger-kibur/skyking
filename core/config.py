import math
import yaml

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

class InstanceListField(ConfigField):
    def __init__(self, instance_class, max_len=None):
        super().__init__([])
        self.iclass = instance_class
        self.max_len = max_len

    def from_raw(self, raw):
        for instance_config in raw:
            new_inst = self.iclass()
            new_inst.config.update_raw(instance_config)
            self.value.append(new_inst)

    def to_raw(self):
        raw_return = []
        for instance in self.value:
            raw_return.append(instance.config.serialize())
        return raw_return

    def append(self, inst):
        if self.validate_inst(inst):
            self.value.append(inst)
        else:
            raise ValueError("Value isn't a valid instance of", self.iclass, "!")
    
    def validate(self, val):
        if type(val) is list:
            return not any([not self.validate_inst(elm) for elm in self.value])
        return False

    def validate_inst(self, val):
        return type(val) is self.iclass      

class InstanceField(InstanceListField):
    def __init__(self, instance_class):
        super().__init__(instance_class, max_len=1)
         

class Config(object):
    def __init__(self, **kwargs):
        self.fields = kwargs

    def update_raw(self, new_val_dict):
        for key, val in new_val_dict.items():
            if key not in self.fields.keys():
                print("Warning: superflous field name", key)
                continue
            self.fields[key].from_raw(val)

    def serialize(self):
        ret_dict = {}
        for key, val in self.fields:
            ret_dict[key] = val.to_raw()
        return ret_dict

class ConfiguredClass(object):

    static_config_table = {}

    @classmethod
    def load_global_config_file(cls, filepath):
        with open(filepath, "r") as file_handle:
            raw = file_handle.read()
        glob_conf_dict = yaml.load(raw)
        for class_key, class_config in glob_conf_dict["static"].items():
            if key not in static_config_table.keys():
                print("Warning: superflous class key in static config file", filepath, ":", key)
                continue
            cls.static_config_table[class_key].update_raw(class_config)

    @classmethod
    def store_global_config_file(cls, filepath):
        

    def __init__(self):
        cls = type(self)
        self.config = cls.static_config_table[cls.get_key()].instant(cls.cur_con)
