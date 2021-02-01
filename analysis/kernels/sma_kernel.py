from . import base_kernel

class SimpleMovingAverageKernel(base_kernel.BaseKernel):
    def __init__(self, kernel_size):
        super().__init__(kernel_size)

    def shift(self, low, high):
        avg = (low + high) / 2
        super().shift(avg)

    def get(self):
        return (self.buffer[-1] - self.buffer[0]) / len(self.buffer)
        