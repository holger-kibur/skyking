

class GuiElement(object):
    @classmethod
    def init_static(cls, cron, style):
        cls.cron = cron

    def __init__(self, **kwargs):
        pass
