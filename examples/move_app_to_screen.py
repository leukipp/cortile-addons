#!/usr/bin/env python3

"""Move app to another screen with global hotkeys.

This script binds hotkeys in the format <ctrl>+<alt>+[SCREEN_INDEX], where SCREEN_INDEX
represents the index of one of the connected screens [see TODO]. The screens are ordered
from left to right (LTR) based on their physical arrangement. When a hotkey is pressed,
the currently active (focused) window will move to the target screen on the same
workspace. Tiling must be enabled on the source and target screens.

Authors:
    * https://github.com/leukipp/

Dependencies:
    The following packages have to be installed::

        $ pip install cortile pynput

Usage:
    Run the python application::

        $ python move_app_to_screen.py

"""


from cortile import Cortile
from pynput import keyboard


def main():

    # init a cortile python object and connect to the running cortile process
    ct = Cortile()

    # TODO: map hotkeys to screen index
    hotkeys = dict()
    for i in range(ct.get_screen_count()):
        hotkeys[f'<ctrl>+<alt>+{i}'] = function_factory(ct, i)

    # bind keyboard shortcuts and callback functions
    with keyboard.GlobalHotKeys(hotkeys) as hotkey:
        hotkey.join()

    # this closes the connection to the running cortile process gracefully
    ct.close()


def function_factory(ct: Cortile, screen_index: int):

    # wrapper function to be attached on hotkey events
    return lambda: move_to_screen(ct, screen_index)


def move_to_screen(ct: Cortile, screen_index: int):

    # extract the active client and window id
    client = ct.get_active_client()
    if not client:
        return

    # x11 window id as integer, other applications may provide the id as hex value 0x...
    window_id = client.Window.Id

    # cortile location (not to be confused with the geometry) of the window, holds the desktop and screen index
    window_location = client.Latest.Location

    # move client window to screen
    if window_location.Screen != screen_index:
        ct.window_to_screen(id=window_id, screen=screen_index)


if __name__ == '__main__':
    main()
