from core import config
from . import security

class Portfolio(config.ConfiguredClass):

    static_config = config.Config()
    instance_config = config.Config(
        securities = config.InstanceListField(security.Security),
    )

    def __init__(self):
        config.ConfiguredClass.__init__(self)