#!/usr/bin/env python3

"""Bind global hotkeys and toggle a layout back and forth.

This script can be used to toggle tiling between a pre-defined layout
and the previous layout. Keyboard shortcuts are registered directly within
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

        $ python toggle_layout_with_keybindings.py

"""


from cortile import Cortile
from pynput import keyboard


# global variable to store the previous layout
PREVIOUS_LAYOUT = None


def main():
    global PREVIOUS_LAYOUT

    # init a cortile python object and connect to the running cortile process
    ct = Cortile()

    # retrieve current active layout
    PREVIOUS_LAYOUT = ct.get_active_layout()

    # TODO: bind keyboard shortcuts and callback functions
    with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+j': lambda: toggle_layout(ct, 'maximized')
    }) as hotkey:
        hotkey.join()

    # this closes the connection to the running cortile process gracefully
    ct.close()


def toggle_layout(ct: Cortile, name: str):
    global PREVIOUS_LAYOUT

    print('<ctrl>+<alt>+j pressed')

    # retrieve current active layout
    active_layout = ct.get_active_layout()
    if not active_layout:
        return

    if PREVIOUS_LAYOUT and active_layout.Name == name:
        # apply the previous layout
        apply_layout(ct, PREVIOUS_LAYOUT.Name, PREVIOUS_LAYOUT.Location.Desktop, PREVIOUS_LAYOUT.Location.Screen)
    else:
        # apply the selected layout
        apply_layout(ct, name, active_layout.Location.Desktop, active_layout.Location.Screen)

    # store the previous layout
    PREVIOUS_LAYOUT = active_layout


def apply_layout(ct: Cortile, name: str, desktop: int, screen: int):

    # the cortile layout names include `-`, where the python methods have them replaced with `_`
    action_execute_name = f'action_execute_layout_{name.replace("-", "_")}'

    # obtain action execute layout method object by name
    action_execute_method = getattr(ct, action_execute_name)

    # apply the selected layout
    action_execute_method(desktop=desktop, screen=screen)


if __name__ == '__main__':
    main()
