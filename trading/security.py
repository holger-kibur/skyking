from core import config

class Security(config.ConfiguredClass):

    cfg_name = "Security"
    cfg = {
        "ticker": config.TickerField(default=None),
        "basis": config.DecimalField(default=0.0, min_=0.01),
        "price_data": config.PriceDataField(default=None),
    }

    def __init__(self):
        super().__init__()