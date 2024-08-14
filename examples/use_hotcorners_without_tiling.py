#!/usr/bin/env python3

"""Use the hotcorner feature to execute custom logic.

This script responds to hotcorner events, which are activated when the pointer
reaches any of the eight hotcorner edges [see TODO]. These events will always
trigger, regardless of whether tiling is enabled. This serves as a basic
template, useful as a starting point if you only wish to use the
hotcorner features without the tiling functionality of cortile.

Authors:
    * https://github.com/leukipp/

Dependencies:
    The following packages have to be installed::

        $ pip install cortile

Usage:
    Run the python application::

        $ python use_hotcorners_without_tiling.py

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

    # the callback will fire on all events, here we are only interested on corner events
    if event.Name == 'Corner':
        handle_hotcorner_activation(ct, event)


def handle_hotcorner_activation(ct: Cortile, event: Dict):

    # receive the corner event data
    corner = event.Data
    if not corner:
        return

    # print the activated corner name, desktop and screen location
    print(f'Corner: {corner.Name}', corner.Location)

    # TODO: run some custom python logic
    if corner.Name == 'top_left':
        pass
    if corner.Name == 'top_center':
        pass
    if corner.Name == 'top_right':
        pass
    if corner.Name == 'center_right':
        pass
    if corner.Name == 'bottom_right':
        pass
    if corner.Name == 'bottom_center':
        pass
    if corner.Name == 'bottom_left':
        pass
    if corner.Name == 'center_left':
        pass


if __name__ == '__main__':
    main()
