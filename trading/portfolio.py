from core import config
from . import security

class Portfolio(config.ConfiguredClass):

    cfg_name = "Portfolio"
    cfg = {
        "name": config.StringField(default="Unnamed"),
        "balance": config.DecimalField(default=0, min_=0),
        "min_liquidity": config.FloatField(default=33, min_=0, max_=100, static=True),
        "securities": config.InstanceListField(security.Security, static=True),
    }

    def __init__(self):
        super().__init__()