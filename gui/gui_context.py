import tkinter as tk
import tkinter.ttk as ttk

class GuiContext(object):
    def __init__(self, trade_ctx):
        self.trade_ctx = trade_ctx
        self.gui_root = tk.Tk()