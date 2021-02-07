from gui import gui_main
from core import loop
from trading import application

mainloop = loop.MainLoop()

app = application.Application()
main_app_gui = gui_main.MainGuiJob(app)

mainloop.loop()