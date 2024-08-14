#!/usr/bin/env python3

"""Swap the active window with the window you are pointing at.

This example demonstrates how to move and swap windows within the active
workspace. A swap event is triggered only if the source and target windows
are on the same desktop and screen. The primary goal of this script is to
illustrate how to access pointer device data and swap windows by setting the
target position [see TODO], which can be any position on the active workspace.

Authors:
    * https://github.com/leukipp/

Dependencies:
    The following packages have to be installed::

        $ pip install cortile

Usage:
    Run the python application::

        $ python swap_apps_using_pointer.py

"""


from cortile import Cortile
from cortile.helper.dict import Dict


def main():

    # init a cortile python object and connect to the running cortile process
    ct = Cortile()

    # listen to cortile events, the lambda function just passes the cortile and event object
    ct.listen(lambda event: event_callback(ct, event))

    # this prevents the main method from exiting and therefore keeps the script running
    ct.wait()


def event_callback(ct: Cortile, event: Dict):

    # the callback will fire on all events, here we are only interested on pointer events
    if event.Name == 'Pointer':
        handle_pointer_clicks(ct, event)


def handle_pointer_clicks(ct: Cortile, event: Dict):

    # receive the pointer event data
    pointer = event.Data
    if not pointer:
        return

    # extract the clicked device button and position on the screen
    button = next((k for k, v in pointer.Device.Button.items() if v), None)
    position = pointer.Device.Position

    # print the clicked device button and position on the screen
    print(f'Pointer: {button}', position)

    # extract the active client and window id
    client = ct.get_active_client()
    if not client:
        return
    window_id = client.Window.Id

    # TODO: move the focused window to the middle click position, which will swap windows
    if button == 'Middle':
        ct.window_to_position(id=window_id, x=position.X, y=position.Y)
    if button == 'Left':
        pass
    if button == 'Right':
        pass


if __name__ == '__main__':
    main()
