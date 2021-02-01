class GuiElement(object):
    def add_self_to_cron(self):
        GuiElement.cron.add_job(self)

def init_gui_static(cron):
    GuiElement.cron = cron