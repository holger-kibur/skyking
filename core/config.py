import math
import yaml
import decimal
import json
import copy

class ConfigInstance:
    def __init__(self, config_ref, table_idx=None):
        self.config_ref = config_ref
        if table_idx is None:
            self.config_ref["dyn_table"].append(
                {key: None for key in self.config_ref["dyn_fields"].keys()}
            )
            self.table_idx = len(self.config_ref["dyn_table"]) - 1
            self.load_defaults()
        else:
            self.table_idx = table_idx
            for key, value in self.config_ref["dyn_table"][table_idx].items():
                deser_value = self.config_ref["dyn_fields"][key].deserialize(value)
                self.config_ref["dyn_table"][table_idx][key] = deser_value

    def load_defaults(self):
        for key, field in self.config_ref["dyn_fields"].items():
            self.config_ref["dyn_table"][self.table_idx][key] = field.pre_process(copy.copy(field.default))

    def close(self):
        self.config_ref["dyn_table"][self.table_idx] = None

    def __getitem__(self, key):
        if key in self.config_ref["static_fields"].keys():
            field = self.config_ref["static_fields"][key]
            value = self.config_ref["static"][key]
        elif key in self.config_ref["dyn_fields"].keys():
            field = self.config_ref["dyn_fields"][key]
            value = self.config_ref["dyn_table"][self.table_idx][key]
        else:
            raise KeyError("Key", key, "not in static or dynamic configuration!")
        return field.post_process(value)

    def __setitem__(self, key, val):
        if key in self.config_ref["static_fields"].keys():
            field = self.config_ref["static_fields"][key]
            table = self.config_ref["static"]
        elif key in self.config_ref["dyn_fields"].keys():
            field = self.config_ref["dyn_fields"][key]
            table = self.config_ref["dyn_table"][self.table_idx]
        else:
            raise KeyError("Key", key, "not in static or dynamic configuration!")
        if not field.validate(val):
            raise ValueError("Value", val, "is not valid for field", field)
        table[key] = field.pre_process(val)

class ConfigAlias:
    def __init__(self, config_ref, table_idx):
        self.config_ref = config_ref
        self.table_idx = table_idx

    def __getitem__(self, key):
        return ConfigInstance.__getitem__(self, key)

    def __setitem__(self, key, val):
        ConfigInstance.__setitem__(self, key, val)

class Configuration(type):

    _config = {}
    pending_config_table_idx = None

    def __init__(cls, name, bases, attribs):
        if name != "ConfiguredClass":
            dyn_fields = {}
            static_fields = {}
            static = {}
            for key, field in attribs["cfg"].items():
                if field.static:
                    static_fields[key] = field
                    static[key] = field.pre_process(field.default)
                else:
                    dyn_fields[key] = field
            new_cfg = {
                "dyn_fields": dyn_fields,
                "static_fields": static_fields,
                "dyn_table": [],
                "static": static,
            }
            cls._config[attribs["cfg_name"]] = new_cfg
        return super().__init__(name, bases, attribs)

    @classmethod
    def store_to_file(cls, filepath):
        serialized = {}
        for cfg_name, cfg in cls._config.items():
            ser_serial = {}
            for key, value in cfg["static"].items():
                ser_serial[key] = cfg["static_fields"][key].serialize(value)
            ser_table = []
            for instance_table in cfg["dyn_table"]:
                ser_instance_table = {}
                for key, value in instance_table.items():
                    ser_instance_table[key] = cfg["dyn_fields"][key].serialize(value)
                ser_table.append(ser_instance_table)
            serialized[cfg_name] = {
                "dyn_table": ser_table,
                "static": ser_serial,
            }
        with open(filepath, "w") as file_handle:
            file_handle.write(json.dumps(serialized, indent=2))

    @classmethod
    def load_from_file(cls, filepath):
        with open(filepath, "r") as file_handle:
            serialized = json.loads(file_handle.read())
        for cfg_name, cfg in serialized.items():
            cls._config[cfg_name]["dyn_table"] = cfg["dyn_table"]
        for cfg_name, cfg in serialized.items():
            for key, value in cfg["static"].items():
                field = cls._config[cfg_name]["static_fields"][key]
                cls._config[cfg_name]["static"][key] = field.deserialize(value)

    @classmethod
    def get_num_instances(cls, iclass):
        return len(cls._config[iclass.cfg_name]["dyn_table"])

    @classmethod
    def get_instance_alias(cls, iclass, index):
        return ConfigAlias(cls._config[iclass.cfg_name], index)

def glob_config_get_instances(iclass):
    return Configuration.get_num_instances(iclass)

def glob_get_instance_alias(iclass, index):
    return Configuration.get_instance_alias(iclass, index)

class ConfiguredClass(metaclass=Configuration):
    def __init__(self):
        self.conf = ConfigInstance(Configuration._config[type(self).cfg_name],
            table_idx = Configuration.pending_config_table_idx,
        )
        Configuration.pending_config_table_idx = None

class ConfigField:
    def __init__(self, default, static=False):
        self.default = default
        self.static = static

    def serialize(self, value):
        return value

    def deserialize(self, value):
        return value

    def pre_process(self, value):
        return value

    def post_process(self, value):
        return value

    def validate(self, value):
        raise NotImplementedError()

class StringField(ConfigField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate(self, value):
        return isinstance(value, str)

class DecimalField(ConfigField):
    def __init__(self, min_=-math.inf, max_=math.inf, places=None, **kwargs):
        super().__init__(**kwargs)
        self.min = min_
        self.max = max_
        self.places = places

    def serialize(self, value):
        return value.to_eng_string()

    def deserialize(self, value):
        return self.pre_process(value)

    def pre_process(self, value):
        new_dec = decimal.Decimal(value)
        return round(new_dec, self.places) if self.places is not None else new_dec

    def validate(self, value):
        try:
            d = decimal.Decimal(value)
        except ValueError:
            return False
        return self.min <= d <= self.max

class FloatField(ConfigField):
    def __init__(self, min_=-math.inf, max_=math.inf, **kwargs):
        super().__init__(**kwargs)
        self.min = min_
        self.max = max_

    def serialize(self, value):
        return str(value)

    def deserialize(self, value):
        return float(value)

    def validate(self, value):
        return isinstance(value, float) and self.min <= value <= self.max

class IntegerField(ConfigField):
    def __init__(self, min_=-math.inf, max_=math.inf, **kwargs):
        super().__init__(**kwargs)
        self.min = min_
        self.max = max_

    def serialize(self, value):
        return str(value)

    def deserialize(self, value):
        return int(value)

    def validate(self, value):
        return isinstance(value, int) and self.min <= value <= self.max

class TickerField(StringField):
    def validate(self, value):
        if not super().validate(value):
            return False
        for char in value:
            if char not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ.":
                return False
        return True

class PriceDataField(ConfigField):
    pass

class ListField(ConfigField):
    def __init__(self, max_len, **kwargs):
        self.max_len = max_len

class InstanceListField(ConfigField):
    def __init__(self, iclass, static=False):
        super().__init__(default=[], static=static)
        self.iclass = iclass

    def serialize(self, value):
        ser_list = []
        for instance in value:
            ser_list.append(instance.conf.table_idx)
        return ser_list
    
    def deserialize(self, value):
        inst_list = []
        for table_idx in value:
            Configuration.pending_config_table_idx = table_idx
            inst_list.append(self.iclass())
        return inst_list

    def validate(self, value):
        return True

class InstanceField(ConfigField):
    def __init__(self, iclass, static=True):
        super().__init__(default=None, static=static)
        self.iclass = iclass

    def serialize(self, value):
        return value.conf.table_idx

    def deserialize(self, value):
        Configuration.pending_config_table_idx = value
        return self.iclass()

    def validate(self, value):
        return isinstance(value, self.iclass)

class BooleanField(ConfigField):
    def serialize(self, value):
        return str(value)
    
    def deserialize(self, value):
        return bool(value)

    def validate(self, value):
        return isinstance(value, bool)