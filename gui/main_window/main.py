import tkinter as tk
import tkinter.ttk as ttk

from .. import gui_element
from core import loop
from util import funcs

class AppMainWindow(ttk.Frame, loop.BaseLoopJob, gui_element.GuiElement):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        loop.BaseLoopJob.__init__(self, 0.5)
        
        control_frame = ttk.Frame(self)
        control_frame.pack(side=tk.TOP, fill=tk.X)

        ttk.Label(control_frame, text="Context Name").pack(side=tk.LEFT)

        self.contexts_combo = ttk.Combobox(control_frame, values=[])
        self.contexts_combo.pack(side=tk.LEFT)

        ttk.Button(control_frame, text="Add", command=self.add_context).pack(side=tk.LEFT)
        
        ttk.Button(control_frame, text="New Context", command=self.create_context).pack(side=tk.RIGHT)

        self.context_panes = ttk.PanedWindow(self, orient=tk.VERTICAL)
        self.context_panes.pack(side=tk.TOP, fill=tk.X)

        self.add_self_to_cron()

    def update_context_list(self):
        pass

    def add_context(self):
        pass

    def create_context(self):
        pass
        
    # Start BaseLoopJob overrides
    def init(self):
        pass

    def run(self):
        self.update_context_list()
    # End BaseLoopJob overrides
