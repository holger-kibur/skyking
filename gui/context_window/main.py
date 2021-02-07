import tkinter as tk
import tkinter.ttk as ttk

from core import loop
from gui.gui_util import graph
from . import portfolio

class ContextMainWindow(ttk.Frame):
    def __init__(self, context):
        self.root = tk.Tk()
        self.root.title("Context")
        self.context = context
        self.value_graph = graph.GoodGraph(self)
        self.value_graph.grid(row=0, column=0, rowspan=2, columnspan=2)
        self.portfolio_view = portfolio.PortfolioFrame(self, context.conf["portfolio"])
        self.portfolio_view.grid(row=1, column=1)