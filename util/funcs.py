

def dict_mask(source, key_list):
    return {key: val for key, val in source.items() if key in key_list}

def destroy_children(self, widget):
    for child in widget.winfo_children():
        child.destroy()

def destroy_widget_list(self, widget_list):
    for widget in widget_list:
        widget.destroy()