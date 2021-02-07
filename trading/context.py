from core import config
from . import portfolio

class TradingContext(config.ConfiguredClass):

    cfg_name = "Context"
    cfg = {
        "portfolio": config.InstanceField(portfolio.Portfolio),
        "friend_name": config.StringField(default="Unnamed Context"),
        "broker_name": config.StringField(default="Unnamed Broker"),
    }
    
    def __init__(self):
        super().__init__()
        