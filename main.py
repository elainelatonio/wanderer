from gui import *

wanderer = Gui()


def close_window():
    global run
    run = False


wanderer.root.protocol("WM_DELETE_WINDOW", close_window)

run = True
while run:
    wanderer.draw_screen()
    wanderer.root.update_idletasks()
    wanderer.root.update()
