from . import base_analyzer
from .. import stock_sig
from ..kernels import eft_kernel, sma_kernel

class ThresholdEftSmaAnalyzer(base_analyzer.BaseAnalyzer):
    def __init__(self, period, threshold):
        self.threshold = threshold
        self.eft = eft_kernel.EhlerFisherKernel(period, 5, 3)
        self.sma = sma_kernel.SimpleMovingAverageKernel(period)
        self.sma_prime = sma_kernel.SimpleMovingAverageKernel(period)
        self.trailing_eft = None
        self.trailing_sma = None

    def shift(self, data):
        self.eft.shift(data.low, data.high)
        self.sma.shift(data.low, data.high)

    def get_signal(self):
        eft_val = self.eft.get()
        sma_val = self.sma.get() * 10
        ret_sig = None
        if self.trailing_eft is None or self.trailing_sma is None or eft_val == sma_val:
            ret_sig = stock_sig.NeutralSignal()
        elif self.trailing_eft < self.trailing_sma and eft_val > sma_val:
            ret_sig = stock_sig.BuySignal(1)
        elif self.trailing_eft > self.trailing_sma and eft_val < sma_val:
            ret_sig = stock_sig.SellSignal(1)
        else:
            ret_sig = stock_sig.NeutralSignal()
        self.trailing_eft = eft_val
        self.trailing_sma = sma_val
        return ret_sig