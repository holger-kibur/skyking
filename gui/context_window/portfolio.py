import tkinter as tk
import tkinter.ttk as ttk

from core import loop, config

class PortfolioFrame(ttk.Frame, config.ConfiguredClass, loop.BaseLoopJob):

    cfg_name = "GUI Portfolio Frame"
    cfg = {
        "update_int": config.FloatField(default=0.5, min_=0.001, static=True),
        "show_profit_percent_day": config.BooleanField(default=True),
        "show_profit_percent_week": config.BooleanField(default=True),
        "show_profit_percent_month": config.BooleanField(default=False),
        "show_profit_dollar_day": config.BooleanField(default=False),
        "show_profit_dollar_week": config.BooleanField(default=False),
        "show_profit_dollar_month": config.BooleanField(default=False),
        "show_current_price": config.BooleanField(default=True),
        "show_basis_price": config.BooleanField(default=True),
        "show_graph": config.BooleanField(default=True),
    }

    def __init__(self, parent, portfolio):
        config.ConfiguredClass.__init__(self)
        loop.BaseLoopJob.__init__(self, self.conf["update_int"])
        ttk.Frame.__init__(self, parent)
        self.portfolio = portfolio

    def make_row(self, row_num, security):
        cc = 0
        ttk.Label(self, text=security.get_name()).grid(row=row_num, column=cc)
        cc += 1
        if self.conf["show_current_price"]:
            ttk.Label(self, text=str(security.get_cur_price())).grid(row=row_num, column=cc)
            cc += 1
        if self.conf["show_basis_price"]:
            ttk.Label(self, text=str(security.get_base_price())).grid(row=row_num, column=cc)
            cc += 1
        if self.conf["show_profit_percent_day"]:
            ttk.Label(self, text=str(security.get_profit_dollar(period=1000 * 3600 * 24)))\
                .grid(row=row_num, column=cc)
            cc += 1
        if self.conf["show_profit_percent_week"]:
            ttk.Label(self, text=str(security.get_profit_dollar(period=1000 * 3600 * 24 * 7)))\
                .grid(row=row_num, column=cc)
            cc += 1
        if self.conf["show_profit_percent_month"]:
            ttk.Label(self, text=str(security.get_profit_dollar(period=1000 * 3600 * 24 * 7 * 31)))\
                .grid(row=row_num, column=cc)
            cc += 1
        if self.conf["show_profit_dollar_day"]:
            ttk.Label(self, text=str(security.get_profit_dollar(period=1000 * 3600 * 24)))\
                .grid(row=row_num, column=cc)
            cc += 1
        if self.conf["show_profit_dollar_week"]:
            ttk.Label(self, text=str(security.get_profit_dollar(period=1000 * 3600 * 24 * 7)))\
                .grid(row=row_num, column=cc)
            cc += 1
        if self.conf["show_profit_dollar_month"]:
            ttk.Label(self, text=str(security.get_profit_dollar(period=1000 * 3600 * 24 * 7 * 31)))\
                .grid(row=row_num, column=cc)
            cc += 1
        if self.conf["show_current_price"]:
            ttk.Label(self, text=str(security.get_cur_price())).grid(row=row_num, column=cc)
            cc += 1

    def init(self):
        for child in self.winfo_children():
            child.destroy()
        cc = 0
        ttk.Label(self, text="Security Name").grid(row=0, column=cc)
        cc += 1
        if self.conf["show_current_price"]:
            ttk.Label(self, text="Current Price").grid(row=0, column=cc)
            cc += 1
        if self.conf["show_basis_price"]:
            ttk.Label(self, text="Basis Price").grid(row=0, column=cc)
            cc += 1
        if self.conf["show_current_price"]:
            ttk.Label(self, text="Current Price").grid(row=0, column=cc)
            cc += 1
        if self.conf["show_profit_percent_day"]:
            ttk.Label(self, text="Profit% Day").grid(row=0, column=cc)
            cc += 1
        if self.conf["show_profit_percent_week"]:
            ttk.Label(self, text="Profit% Week").grid(row=0, column=cc)
            cc += 1
        if self.conf["show_profit_percent_month"]:
            ttk.Label(self, text="Profit% Month").grid(row=0, column=cc)
            cc += 1
        if self.conf["show_profit_dollar_day"]:
            ttk.Label(self, text="Profit$ Day").grid(row=0, column=cc)
            cc += 1
        if self.conf["show_profit_dollar_week"]:
            ttk.Label(self, text="Profit$ Week").grid(row=0, column=cc)
            cc += 1
        if self.conf["show_profit_dollar_month"]:
            ttk.Label(self, text="Profit$ Month").grid(row=0, column=cc)
            cc += 1
        for i, security in enumerate(self.portfolio.conf["securities"]):
            self.make_row(i + 1, security)

    def run(self):
        

