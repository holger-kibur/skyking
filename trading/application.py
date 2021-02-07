from core import config
from . import context

class Application(config.ConfiguredClass):

    cfg_name = "Application"
    cfg = {
        "contexts": config.InstanceListField(context.TradingContext, static=True)
    }

    def __init__(self):
        super().__init__()

    def create_context(self):
        self.conf["contexts"].append(context.TradingContext())