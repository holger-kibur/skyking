import math
import yaml

from util import funcs

class ConfigInstance:
    def __init__(self, config_ref):
        self.config_ref = config_ref
        self.config_ref.dyn_table.append([None] * len(self.config_ref.field_keys))
        self.table_idx = len(self.config_ref) - 1
        self.load_defaults()

    def load_defaults(self):
        for key, field in self._config_ref.fields:
            self.config_ref.dyn_table[self.table_idx][key] = field.default

    def __getitem__(self, key):
        if key in self.config_ref.static.keys():
            return self.config_ref.static[key]
        elif key in self.config_ref.dyn_table[self.table_idx].keys():
            return self.config_ref.dyn_table[self.table_idx][key]
        else:
            raise KeyError("Key", key, "not in static or dynamic configuration!")

class Configuration(type):

    _config = {}

    def __init__(cls, name, bases, attribs):
        if name != "ConfiguredClass":
            dyn_fields = {}
            static_fields = {}
            static = {}
            for key, field in attribs["cfg"]:
                if field.static:
                    static_fields[key] = field
                    static[key] = field.default
                else:
                    dyn_fields[key] = field
            new_cfg = {
                "dyn_fields": dyn_fields,
                "static_fields": static_fields,
                "dyn_table": [],
                "static": static,
            }
            cls._config[attribs["cfg_name"]] = new_cfg
        return super().__init__(cls, name, bases, attribs)

    def __call__(cls, *args, _config_inst=None, **kwargs):
        cls._cfg_reference

class ConfiguredClass(metaclass=Configuration):
    pass