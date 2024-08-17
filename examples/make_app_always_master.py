#!/usr/bin/env python3

"""Make a specific application always master.

When cortile is running and a pre-defined application is launched,
it will make the application a master window on the current layout.
The application will be selected based on the class name(s), which
are passed as command line arguments [see TODO]. Applications
will be made master only if there where just recently opened.

Authors:
    * https://github.com/leukipp/

Dependencies:
    The following packages have to be installed::

        $ pip install cortile

Usage:
    Run the python application (TODO: pass class names of applications).
    Within the cortile 'addons' folder this script will not work, since
    arguments can't be passed.::

        $ python make_app_always_master.py firefox code

"""

import sys
from typing import List
from cortile import Cortile
from cortile.helper.dict import Dict
from cortile.helper.time import Time


# helper variable to store the last event time
event_time = Time()


def main(args):

    # init a cortile python object and connect to the running cortile process
    ct = Cortile()

    # listen to cortile events, the lambda function just passes the cortile, event and args object
    ct.listen(lambda event: event_callback(ct, event, args))

    # this prevents the main method from exiting and therefore keeps the script running
    ct.wait()


def event_callback(ct: Cortile, event: Dict, args: List[str]):

    # the callback will fire on all events, here we are only interested on client changes
    if event.Name == 'Clients':
        handle_clients_change(ct, event, args)


def handle_clients_change(ct: Cortile, event: Dict, args: List[str]):

    # to prevent multiple executions, we’ll ignore additional client events triggered by our own logic
    if event_time.delta().seconds < 1:
        return

    # windows classes passed as list of argument strings
    window_classes = [x.lower() for x in args]

    # the event data values contains a list with all tracked cortile clients
    for client in event.Data.Values:

        # x11 window id as integer, other applications may provide the id as hex value 0x...
        window_id = client.Window.Id

        # x11 window class name, based on this we can filter all application instances of this type
        window_class = client.Latest.Class.lower()

        # cortile location (not to be confused with the geometry) of the window, holds the desktop and screen index
        window_location = client.Latest.Location

        # cortile creation timestamp in ms, is the time at which the client was tracked internally
        window_timestamp = client.Window.Created

        # timedelta relative to now, to determine whether the window has just been recently opened
        window_lifetime = Time(window_timestamp).delta()

        # lets check if one of the clients match and they have just been recently (in the last 3s) added
        if window_class in window_classes and window_lifetime.seconds < 3:

            # this moves the focus to the window
            ct.window_activate(id=window_id)

            # the focused window will be made a master, the desktop and screen index must be provided
            ct.action_execute_master_make(desktop=window_location.Desktop, screen=window_location.Screen)

            # update the global event time object
            event_time.set(event.Time)


if __name__ == '__main__':
    main(sys.argv)
