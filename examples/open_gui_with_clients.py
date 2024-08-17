#!/usr/bin/env python3

"""Open a python gui window showing a list of clients.

This example opens a python gui built with tkinter to display a list of clients present
on the currently active screen. Each client is represented by a simple button, which when
clicked, triggers a pre-defined cortile event. In this case [see TODO], the event will
make the window a master. The script demonstrates how to retrieve screen geometry,
which is used here to position the gui window at the center of the screen.

Authors:
    * https://github.com/leukipp/

Dependencies:
    The following packages have to be installed::

        $ apt install python3-tk
        $ pip install cortile

Usage:
    Run the python application::

        $ python open_gui_with_clients.py

"""


import tkinter as tk
from cortile import Cortile


def main():

    # init a cortile python object and connect to the running cortile process
    ct = Cortile()

    # retrieve the screen dimension of the currently active screen
    screens = ct.get_screen_dimensions()
    screen_index = ct.get_active_screen()
    screen_dimension = screens[screen_index].Geometry

    # calculate the tkinter window position
    window_w = 400
    window_h = 400
    window_x = screen_dimension.X + screen_dimension.Width // 2 - window_w // 2
    window_y = screen_dimension.Y + screen_dimension.Height // 2 - window_h // 2

    # create a tkinter window positioned at the center of the screen
    window = tk.Tk()
    window.title('cortile-addons')
    window.geometry(f'{window_w}x{window_h}+{window_x}+{window_y}')
    window.overrideredirect(True)
    window.resizable(False, False)
    window.configure(bg='white')

    # tkinter button to close the window
    tk.Button(window, text='[CLOSE GUI]', command=window.destroy).pack()

    # retrieve clients on the current active desktop and screen
    for client in ct.get_active_clients():
        window_id = client.Window.Id
        client_name = client.Latest.Name
        client_class = client.Latest.Class

        # TODO: tkinter button to make window master
        button_text = f'{client_class} - {client_name}'[:40]
        tk.Button(window, text=f'{button_text}...', command=function_factory(ct, window_id)).pack()

    # start the tkinter event loop
    window.mainloop()

    # this closes the connection to the running cortile process gracefully
    ct.close()


def function_factory(ct: Cortile, window_id: int):

    # wrapper function to be attached on hotkey events
    return lambda: master_make(ct, window_id)


def master_make(ct: Cortile, window_id: int):

    # retrieve current active desktop and screen index
    active_desktop = ct.get_active_desktop()
    active_screen = ct.get_active_screen()

    # activate the clicked client and make it a master window
    ct.window_activate(id=window_id)
    ct.action_execute_master_make(desktop=active_desktop, screen=active_screen)


if __name__ == '__main__':
    main()
