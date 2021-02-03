from core import config
from . import portfolio

class TradingContext(config.ConfiguredClass):

    static_config = config.Config()
    instance_config = config.Config(
        portfolio = config.InstanceField(portfolio.Portfolio),
    )

    def __init__(self):
        config.ConfiguredClass.__init__(self)
        if 