import tkinter as tk
import tkinter.ttk as ttk

from core import config
from trading import context
from . import context_pane

class AppMainWindow(ttk.Frame):
    def __init__(self, parent, app_ref):
        ttk.Frame.__init__(self, parent, padding="0.1i")
        
        self.app_ref = app_ref

        control_frame = ttk.Frame(self)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(control_frame, text="Context Name:").pack(side=tk.LEFT)

        self.contexts_combo = ttk.Combobox(control_frame, values=[])
        self.contexts_combo.pack(side=tk.LEFT)

        ttk.Button(control_frame, text="Add", command=self.add_context).pack(side=tk.LEFT)
        
        ttk.Button(control_frame, text="New Context", command=self.create_context).pack(side=tk.RIGHT)

        self.context_panes = ttk.Frame(self)
        self.context_panes.pack(side=tk.TOP, fill=tk.X)

    def update_context_list(self):
        for child in self.context_panes.winfo_children():
            child.del_self_from_cron()
            child.destroy()
        for context in self.app_ref.conf["contexts"]:
            context_pane.ContextPaneFrame(self.context_panes, context).pack(side=tk.TOP, fill=tk.X)

    def add_context(self):
        pass

    def create_context(self):
        self.app_ref.create_context()
        self.update_context_list()