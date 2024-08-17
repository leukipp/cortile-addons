#!/usr/bin/env python3

"""Apply a layout and disable tiling afterwards.

You can use this script in cases where you only want to maximize
windows once and disable tiling afterwards. The active desktop and
screen index is determined by the current position of the mouse. At first
tiling will be enabled, then maximization will be applied [see TODO].
Afterwards tiling is disabled and windows are in stacking mode again.

Authors:
    * https://github.com/leukipp/

Dependencies:
    The following packages have to be installed::

        $ pip install cortile

Usage:
    Run the python application::

        $ python apply_layout_and_disable.py

"""


from cortile import Cortile


def main():

    # init a cortile python object and connect to the running cortile process
    ct = Cortile()

    # retrieve current active desktop index
    desktop_index = ct.get_active_desktop()

    # retrieve current active screen index
    screen_index = ct.get_active_screen()

    # enable tiling, just in case it was disabled (since cortile actions will be otherwise ignored)
    ct.action_execute_enable(desktop=desktop_index, screen=screen_index)

    # TODO: change to your desired layout
    ct.action_execute_layout_maximized(desktop=desktop_index, screen=screen_index)

    # disable tiling, but leave all windows at there latest position
    ct.action_execute_disable(desktop=desktop_index, screen=screen_index)

    # this closes the connection to the running cortile process gracefully
    ct.close()


if __name__ == '__main__':
    main()
