import matplotlib.pyplot as pyplot
import matplotlib.axes as axes
import math
import pandas
import json
import kernels.sma_kernel as sma

class EhlerFisherKernel(object):
    def __init__(self, kernel_size, inter_ema_size, eft_ema_size):
        self.kernel_size = kernel_size
        self.inter_ema_size = inter_ema_size
        self.eft_ema_size = eft_ema_size
        self.price_buffer = []
        self.inter_ema = 0
        self.eft_ema = 0
    
    def shift(self, new_low, new_high):
        if len(self.price_buffer) >= self.kernel_size:
            self.price_buffer.pop(0)
        self.price_buffer.append((new_low, new_high))

        price_min, price_max = math.inf, 0
        for low, high in self.price_buffer:
            price_min = min(low, price_min)
            price_max = max(high, price_max)
        
        avg = (new_low + new_high) / 2
        inter = (avg - price_min) / (price_max - price_min) - 0.5
        self.inter_ema += (2 / (self.inter_ema_size + 1)) * (inter * 2 - self.inter_ema)

        eft = math.log((1 + self.inter_ema) / (1 - self.inter_ema))
        self.eft_ema += (2 / (self.eft_ema_size + 1)) * (eft - self.eft_ema)

    def get_eft(self):
        return self.eft_ema

class DeltaKernel(object):
    def __init__(self, kernel_size):
        self.kernel_size = kernel_size
        self.roc_ema = 0
        self.last_price = 0
        # Make this into exponential weighted average delta kernel

    def shift(self, new_low, new_high):
        avg_price = (new_low + new_high) / 2
        roc = avg_price - self.last_price
        self.last_price = avg_price
        
        self.roc_ema += (2 / (self.kernel_size + 1)) * (roc - self.roc_ema)
        
    def get_roc(self):
        return self.roc_ema

class VolatilityKernel(object):
    def __init__(self, kernel_size):
        self.kernel_size = kernel_size
        self.roc_buffer = []
        self.mean = 0
        self.std = 0

    def shift(self, roc):
        if len(self.roc_buffer) == self.kernel_size:
            popped_roc = self.roc_buffer.pop(0)
        else:
            popped_roc = 0
        self.roc_buffer.append(roc)

        if len(self.roc_buffer) < 2:
            return

        self.mean = 0
        self.std = 0
        for val in self.roc_buffer:
            self.mean += val / len(self.roc_buffer)
        for val in self.roc_buffer:
            self.std += (val - self.mean) ** 2
        self.std = math.sqrt(self.std / (len(self.roc_buffer) - 1))

    def get_sigma(self):
        return self.std

def main(eft_ksize, inter_ema, eft_ema, roc_ksize, roc_mult):
    with open("../sample_mrvl.txt", "r") as f:
        data_dict = json.loads(f.read())
    data = pandas.DataFrame.from_dict(data_dict)

    kernel = EhlerFisherKernel(eft_ksize, inter_ema, eft_ema)
    sec_kern = EhlerFisherKernel(roc_ksize, inter_ema, eft_ema)
    roc_kernel = sma.SimpleMovingAverageKernel(roc_ksize)
    vol_kernel = VolatilityKernel(144)

    eft_column = []
    roc_column = []
    vol_column = []

    theo_column = []
    last_avg = None
    ideal_ratio = 1
    trailing_high = None
    trailing_low = None
    for _, row in data.iterrows():
        avg = (row["Low"] + row["High"]) / 2
        if last_avg is not None:
            this_rat = avg / last_avg
            if this_rat > 1:
                ideal_ratio *= this_rat
        last_avg = avg
        theo_column.append(ideal_ratio)
        
        kernel.shift(row["Low"], row["High"])
        if trailing_high is None:
            trailing_high = row["High"]
            trailing_low = row["Low"]
            sec_kern.shift(0, 1)
        else:
            sec_kern.shift(row["Low"] - trailing_low, row["High"] - trailing_high)
            trailing_high = row["High"]
            trailing_low = row["Low"]
        roc_kernel.shift(row["Low"], row["High"])
        eft_column.append(kernel.get_eft())
        roc_column.append(roc_kernel.get() * 10)
        # vol_kernel.shift(roc_kernel.get_roc() * 10)
        sig = vol_kernel.get_sigma()
        vol_column.append(sig)
    data["EFT"] = eft_column
    data["ROC"] = roc_column
    # data["VOL"] = vol_column
    data["THEO"] = theo_column

    account_column = []
    buy_column = []
    last_roc = 0
    last_eft = 0
    buy_price = 0
    principle = 1
    last_order = 0
    min_order_interval = math.inf
    for index, row in data.iterrows():
        index = int(index)
        ratio = 0
        avg = (row["High"] + row["Low"]) / 2
        if last_eft < last_roc and row["EFT"] >= row["ROC"]:
            ratio = -1
            buy_price = avg
        elif last_eft > last_roc and row["EFT"] <= row["ROC"]:
            if buy_price == 0:
                buy_price = avg
            ratio = avg / buy_price
            principle *= ratio
        elif last_roc < -3:
            if buy_price == 0:
                buy_price = avg
            ratio = avg / buy_price
            principle *= ratio
        if ratio != 0:
            # print(index - last_order)
            last_order = index
        account_column.append(principle)
        buy_column.append(ratio)
        last_roc = row["ROC"]
        last_eft = row["EFT"]
    data["ACC"] = account_column
    data["BUY"] = buy_column

    _, (ax1, ax2, ax3, ax4) = pyplot.subplots(4, sharex=True)
    data.plot(y=["Low", "High"], ax=ax1)
    data.plot(y=["EFT", "ROC"], ax=ax2, ylim=(-4, 4))
    data.plot(y=["ACC", "BUY"], ax=ax3)
    data.plot(y="THEO", ax=ax4)

    pyplot.show()

    return principle

print(main(30, 5, 3, 30, 30))