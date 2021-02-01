from gui import gui_element, gui_main
from core import loop

mainloop = loop.MainLoop()
gui_element.init_gui_static(mainloop)

main_app_gui = gui_main.MainGuiJob()

mainloop.loop()