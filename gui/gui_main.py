import tkinter as tk
import time

from core import loop, config
from trading import application
from . import gui_context
from .main_window import main as gui

class MainGuiJob(loop.BaseLoopJob, config.ConfiguredClass):

    cfg_name = "GUI Main Job"
    cfg = {
        "tk_update_int": config.FloatField(default=0.05, min_=0.001, static=True),
        "window_width": config.IntegerField(default=640, min_=240, max_=1920, static=True),
        "window_height": config.IntegerField(default=640, min_=240, max_=1080, static=True),
    }

    def __init__(self, app_ref):
        config.ConfiguredClass.__init__(self)
        loop.BaseLoopJob.__init__(self, self.conf["tk_update_int"])
        self.app_ref = app_ref
        self.gui_root = None
        self.context_roots = []
        self.add_self_to_cron()
        
    # Start BaseLoopJob overrides
    def init(self):
        self.gui_root = tk.Tk()
        self.gui_root.title("Trading Application")
        self.gui_root.protocol("WM_DELETE_WINDOW", self.close)
        self.gui_root.geometry(f"{self.conf['window_width']}x{self.conf['window_height']}")
        gui.AppMainWindow(self.gui_root, self.app_ref).pack(fill=tk.BOTH)

    def run(self):
        self.gui_root.update_idletasks()
        self.gui_root.update()
        for ctx_root in self.context_roots:
            ctx_root.update_idletasks()
            ctx_root.update()

    def close(self):
        self.gui_root.destroy()
        loop.BaseLoopJob.close(self)
    # End BaseLoopJob overrides