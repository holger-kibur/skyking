import tkinter as tk
import tkinter.ttk as ttk

from util import funcs

class GridSquare(ttk.Frame):
    def __init__(self, parent, get_method, inst):
        super().__init__(parent)
        self.inst = inst
        self.get_method = get_method
        self.int_widget = self.get_method(inst)
        self.int_widget.pack(fill=tk.BOTH)

    def update(self):
        self.int_widget.destroy()
        self.int_widget = self.get_method(inst)
        self.int_widget.pack(fill=tk.BOTH)

class TableFrame(ttk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.columns = {}
        self.col_order = []
        self.row_insts = []
        self.header_frame = ttk.Frame(self)
        self.content_frames = []
        self.seperator = ttk.Seperator(self, orient=tk.HORIZONTAL)

    def add_column(self, key, name, unbound_access):
        self.columns[key] = (name, unbound_access)
        self.col_order.append(key)

    def add_row(self, instance):
        self.row_insts.append(instance)

    def reset_layout(self):
        funcs.destroy_children(self.header_frame)
        funcs.destroy_widget_list(self.content_frames)
        for csquare in self.content_squares:
            csquare.destroy()
        for i, col_key in enumerate(self.col_order):
            ttk.Label(self, text=self.columns[col_key][0]).grid(row=0, column=i)
            content_frame = ttk.Frame(self)
            content_frame.grid(row=2, column=i)
            self.content_frames.append(content_frame)
            for inst in self.row_insts:
                GridSquare(content_frame, self.columns[col_key][1], inst).pack(side=tk.TOP)
        self.seperator.grid_forget()
        self.seperator.grid(row=1, column=0, columnspan=len(self.col_order), sticky=tk.EW)

    def update_info(self):
        for content_frame in self.content_frames:
            for content_square in content_frame.winfo_children():
                content_square.update()
