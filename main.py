from gui import *

wanderer = Gui()
while True:
    wanderer.draw_screen()
    wanderer.root.update_idletasks()
    wanderer.root.update()
