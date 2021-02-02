from core import config

class GuiElement(object):

    cron = None
    config_table = {}

    def __init__(self):
        subclass = type(self)
        if "static_config" in subclass.__dict__.keys():
            if hash(subclass) in config_table.keys():
                print("Warning: Duplicate static configuration created", hash(subclass))
            config_table[subclass] = subclass.static_config
        self.config = subclass.static_config

    def add_self_to_cron(self):
        GuiElement.cron.add_job(self)

    def __hash__(self):
        return type(self).__name__

def init_gui_static(cron):
    GuiElement.cron = cron
