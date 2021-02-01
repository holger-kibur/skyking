

class BaseKernel(object):
    def __init__(self, kernel_size):
        self.kernel_size = kernel_size
        self.buffer = []
    
    def shift(self, *args):
        popped = None
        if len(self.buffer) >= self.kernel_size:
            popped = self.buffer.pop(0)
        if args:
            self.buffer.append(args[0] if len(args) == 1 else args)
        return popped

    def get(self):
        raise NotImplementedError

    def set_kernel_size(self, kernel_size):
        if kernel_size < self.kernel_size:
            self.buffer = self.buffer[-kernel_size:]
        self.kernel_size = kernel_size