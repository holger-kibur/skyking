from core import config
from . import security

class Portfolio(config.ConfiguredClass):

    cfg_name = "User Portfolio"
    cfg = config.Configuration(Portfolio,
        name = config.StringField(default="Unnamed"),
        balance = config.DecimalField(default=0, min=0),
        min_liquidity = config.DecimalField(default=33, min=0, max=100, places=2, static=True),
    )

    def __init__(self):
        super().__init__()