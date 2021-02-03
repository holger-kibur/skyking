from core import config

class Security(config.ConfiguredClass):

    static_config = config.Config()
    instance_config = config.Config(
        ticker = config.TickerField(),
        basis = config.DecimalField(min = 0.01),
        price_data = config.PriceDataField(),
    )

    def __init__(self):
        config.ConfiguredClass.__init__(self)