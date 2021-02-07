import tkinter as tk

class GoodGraph(tk.Canvas):
    def __init__(self, parent):
        super().__init__(self, parent, bg="white")
        
    def plot_data(self, data, data_keys):
        for key in data_keys:
            