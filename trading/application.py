from core import config
from . import context

class Application(config.ConfiguredClass):

    static_config = config.Config(
        contexts = config.InstanceListField(context.TradingContext)
    )

    def __init__(self):
        config.ConfiguredClass.__init__(self)

    def new_context(self):
        self.config.contexts.append(context.TradingContext())