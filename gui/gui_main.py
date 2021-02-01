import tkinter as tk

from core import loop
from . import gui_context, gui_element
from .main_window import main as gui

class MainGuiJob(loop.BaseLoopJob, gui_element.GuiElement):
    def __init__(self):
        super().__init__(50)
        self.contexts = []
        self.gui_root = None

    def add_context(self, trade_ctx):
        self.contexts.append(gui_context.GuiContext(trade_ctx))
        
    def init(self):
        self.gui_root = tk.Tk()
        self.gui_root.title("Trading Application")
        gui.AppMainWindow(self.gui_root).pack(fill=tk.BOTH)

    def 