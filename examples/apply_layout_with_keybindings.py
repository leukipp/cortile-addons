#!/usr/bin/env python3

"""Bind global hotkeys and apply a layout.

This script is designed for one-time window arrangement followed
by disabling tiling. Keyboard shortcuts are registered directly within
the python script [see TODO], therefore bypassing cortile key bindings.
The script will wait for global hotkey events, which executes python
callback functions that will trigger your desired cortile logic.

Authors:
    * https://github.com/leukipp/

Dependencies:
    The following packages have to be installed::

        $ pip install cortile pynput

Usage:
    Run the python application::

        $ python apply_layout_with_keybindings.py

"""


from cortile import Cortile
from pynput import keyboard


def main():

    # init a cortile python object and connect to the running cortile process
    ct = Cortile()

    # TODO: bind keyboard shortcuts and callback functions
    with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+i': lambda: key_callback_i(ct),
        '<ctrl>+<alt>+j': lambda: key_callback_j(ct)
    }) as hotkey:
        hotkey.join()

    # this closes the connection to the running cortile process gracefully
    ct.close()


def key_callback_i(ct: Cortile):
    print('<ctrl>+<alt>+i pressed')

    # apply the horizontal-top layout
    apply_layout(ct, 'horizontal_top')


def key_callback_j(ct: Cortile):
    print('<ctrl>+<alt>+j pressed')

    # apply the vertical-right layout
    apply_layout(ct, 'vertical_right')


def apply_layout(ct: Cortile, name: str):

    # retrieve current active desktop/workspace index
    desktop_index = ct.get_active_workspace()

    # retrieve current active screen index
    screen_index = ct.get_active_screen()

    # enable tiling, just in case it was disabled (since cortile actions will be otherwise ignored)
    ct.action_execute_enable(desktop=desktop_index, screen=screen_index)

    # apply the selected layout
    if name == 'horizontal_top':
        ct.action_execute_layout_horizontal_top(desktop=desktop_index, screen=screen_index)
    elif name == 'vertical_right':
        ct.action_execute_layout_vertical_right(desktop=desktop_index, screen=screen_index)

    # disable tiling, but leave all windows at there latest position
    ct.action_execute_disable(desktop=desktop_index, screen=screen_index)


if __name__ == '__main__':
    main()
