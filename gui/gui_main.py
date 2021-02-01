import tkinter as tk
import time

from core import loop
from . import gui_context, gui_element
from .main_window import main as gui

class MainGuiJob(loop.BaseLoopJob, gui_element.GuiElement):
    def __init__(self):
        loop.BaseLoopJob.__init__(self, 0.05)
        self.gui_contexts = []
        self.gui_root = None
        self.add_self_to_cron()

    def add_gui_context(self, trade_ctx):
        self.gui_contexts.append(gui_context.GuiContext(trade_ctx))
        
    # Start BaseLoopJob overrides
    def init(self):
        self.gui_root = tk.Tk()
        self.gui_root.title("Trading Application")
        self.gui_root.protocol("WM_DELETE_WINDOW", self.close)
        gui.AppMainWindow(self.gui_root).pack(fill=tk.BOTH)

    def run(self):
        self.gui_root.update_idletasks()
        self.gui_root.update()
        for context in self.gui_contexts:
            context.update()

    def close(self):
        self.gui_root.destroy()
        super().close()
    # End BaseLoopJob overrides