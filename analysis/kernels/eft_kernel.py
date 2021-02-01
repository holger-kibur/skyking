import math
from . import base_kernel

class EhlerFisherKernel(base_kernel.BaseKernel):
    def __init__(self, kernel_size, inter_ema_size, eft_ema_size):
        super().__init__(kernel_size)
        self.inter_ema_size = inter_ema_size
        self.eft_ema_size = eft_ema_size
        self.inter_ema = 0
        self.eft_ema = 0

    def shift(self, low, high):
        super().shift(low, high)

        price_min, price_max = math.inf, 0
        for low, high in self.buffer:
            price_min = min(low, price_min)
            price_max = max(high, price_max)
        
        avg = (low + high) / 2
        inter = (avg - price_min) / (price_max - price_min) - 0.5
        self.inter_ema += (2 / (self.inter_ema_size + 1)) * (inter * 2 - self.inter_ema)

        eft = math.log((1 + self.inter_ema) / (1 - self.inter_ema))
        self.eft_ema += (2 / (self.eft_ema_size + 1)) * (eft - self.eft_ema)

    def get(self):
        return self.eft_ema

    def set_inter_len(self, inter_ema_size):
        self.inter_ema_size = inter_ema_size

    def set_eft_len(self, eft_ema_size):
        self.eft_ema_size = eft_ema_size