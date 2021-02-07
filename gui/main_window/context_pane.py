import tkinter as tk
import tkinter.ttk as ttk

from core import config, loop

class ContextPaneFrame(ttk.Frame, loop.BaseLoopJob, config.ConfiguredClass):

    cfg_name = "GUI Context Pane"
    cfg = {
        "update_int": config.FloatField(default=0.5, min_=0.001, static=True),
    }

    def __init__(self, parent, context):
        ttk.Frame.__init__(self, parent, padding="0.25i")
        config.ConfiguredClass.__init__(self)
        loop.BaseLoopJob.__init__(self, self.conf["update_int"])
        self.context = context
        self.friend_name_label = ttk.Label(self)
        self.friend_name_label.grid(row=0, column=0)
        self.broker_name_label = ttk.Label(self)
        self.broker_name_label.grid(row=0, column=1)
        self.add_self_to_cron()

    def run(self):
        self.friend_name_label.config(text=self.context.conf["friend_name"])
        self.broker_name_label.config(text=self.context.conf["broker_name"])
