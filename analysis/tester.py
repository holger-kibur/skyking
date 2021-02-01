import pandas
import json
import matplotlib.pyplot as pyplot

from .analyzers import simple_eft_sma
from . import stock_sig

PERIOD = 150

with open("sample_gme.txt", "r") as f:
    data_dict = json.loads(f.read())
data = pandas.DataFrame.from_dict(data_dict)
data["low"] = data["Low"]
data["high"] = data["High"]

simple = simple_eft_sma.SimpleEftSmaAnalyzer(PERIOD)

principle = 1
buy_price = None
for _, row in data.iterrows():
    avg = (row.low + row.high) / 2
    simple.shift(row)
    sig = simple.get_signal()
    if sig == stock_sig.BuySignal:
        buy_price = avg
    elif sig == stock_sig.SellSignal and buy_price is not None:
        principle *= avg / buy_price
print(principle)
