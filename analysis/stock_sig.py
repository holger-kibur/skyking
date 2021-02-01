from util import enum

class NeutralSignal(enum.Enum):
    pass

class BuySignal(enum.Enum):
    def __init__(self, confidence):
        self.confidence = confidence

class SellSignal(enum.Enum):
    def __init__(self, confidence):
        self.confidence = confidence