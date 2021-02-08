import tkinter as tk
import tkinter.ttk as ttk

from core import loop, config
from trading import security
from gui.gui_util import table, graph

class PortfolioFrame(ttk.Frame, config.ConfiguredClass, loop.BaseLoopJob):

    cfg_name = "GUI Portfolio Frame"
    cfg = {
        "update_int": config.FloatField(default=0.5, min_=0.001, static=True),
        "displayed_figs": config.ListField(default=["cp", "bp", "tp", "dpp", "wpp", "pg"]),
    }

    key_name_method_lookup = {
        "name": ("Security Name", security.Security.get_name),
        "cp": ("Current Price", security.Security.get_cur_price),
        "bp": ("Basis Price", security.Security.get_basis_price),
        "tp": ("Total Profit", security.Security.get_total_profit),
        "dpp": ("Day P%", lambda inst: security.Security.get_price_percent(inst, from_=1000*3600*24)),
        "wpp": ("Week P%", lambda inst: security.Security.get_price_percent(inst, from_=1000*3600*24*7)),
        "mpp": ("Month P%", lambda inst: security.Security.get_price_percent(inst, from_=1000*3600*24*7*31)),
        "dpd": ("Day P$", lambda inst: security.Security.get_price_dollar(inst, from_=1000*3600*24)),
        "wpd": ("Week P$", lambda inst: security.Security.get_price_dollar(inst, from_=1000*3600*24*7)),
        "mpd": ("Month P$", lambda inst: security.Security.get_price_dollar(inst, from_=1000*3600*24*7*31)),
        "pg": ("Price Graph", lambda inst: security.Security.get_price_data(inst)),
    }

    def __init__(self, parent, portfolio):
        config.ConfiguredClass.__init__(self)
        loop.BaseLoopJob.__init__(self, self.conf["update_int"])
        ttk.Frame.__init__(self, parent)
        self.portfolio = portfolio
        self.security_table = table.TableFrame(self)
        self.security_table.pack(side=tk.TOP, fill=tk.BOTH)

    def wrap_with_label(self, in_func):
        def dispatch(inst):
            return ttk.Label(self.security_table, text=str(in_func(inst)))
        return dispatch

    def wrap_with_graph(self, in_func):
        def dispatch(inst):
            return graph.GoodGraph(self.security_table, data=in_func(inst))
        return dispatch

    def init(self):
        for col_key in ["name"] + self.conf["displayed_figs"]:
            col_name, col_meth = type(self).key_name_method_lookup[col_key]
            if col_key != "pg":
                self.security_table.add_column(col_key, col_name, self.wrap_with_label(col_meth))
            else:
                self.security_table.add_column(col_key, col_name, self.wrap_with_graph(col_meth))

    def run(self):
        self.security_table.update_info()

