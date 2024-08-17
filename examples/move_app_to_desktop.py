#!/usr/bin/env python3

"""Automatically open applications on specific desktop.

When cortile is running and a pre-defined application is launched,
it will automatically relocate the application to a designated desktop.
This behavior is determined by the applications class name(s). Both the class
name(s) and the target desktop are hardcoded into the system [see TODO]. This
ensures that each application is consistently moved to its appropriate desktop.

Authors:
    * https://github.com/leukipp/

Dependencies:
    The following packages have to be installed::

        $ pip install cortile

Usage:
    Run the python application::

        $ python move_app_to_desktop.py

"""


from cortile import Cortile
from cortile.helper.dict import Dict
from cortile.helper.time import Time


# helper variable to store the last event time
event_time = Time()


def main():

    # init a cortile python object and connect to the running cortile process
    ct = Cortile()

    # listen to cortile events, the lambda function just passes the cortile and event object
    ct.listen(lambda event: event_callback(ct, event))

    # this prevents the main method from exiting and therefore keeps the script running
    ct.wait()


def event_callback(ct: Cortile, event: Dict):

    # the callback will fire on all events, here we are only interested on client changes
    if event.Name == 'Clients':
        handle_clients_change(ct, event)


def handle_clients_change(ct: Cortile, event: Dict):

    # to prevent multiple executions, we’ll ignore additional client events triggered by our own logic
    if event_time.delta().seconds < 1:
        return

    # TODO: change desktop index and window classes to your preferences
    desktop_index = 1
    window_classes = ['firefox']

    # the event data values contains a list with all tracked cortile clients
    for client in event.Data.Values:

        # x11 window id as integer, other applications may provide the id as hex value 0x...
        window_id = client.Window.Id

        # x11 window class name, based on this we can filter all application instances of this type
        window_class = client.Latest.Class

        # cortile location (not to be confused with the geometry) of the window, holds the desktop and screen index
        window_location = client.Latest.Location

        # cortile creation timestamp in ms, is the time at which the client was tracked internally
        window_timestamp = client.Window.Created

        # timedelta in relation to now, to determine whether the window has just been opened recently
        window_lifetime = Time(window_timestamp).delta()

        # lets check if one of the clients match and they have just been recently (in the last 3s) added
        if window_class in window_classes and window_lifetime.seconds < 3:

            # move the window to the pre-defined desktop index
            if window_location.Desktop != desktop_index:
                ct.window_to_desktop(id=window_id, desktop=desktop_index)

                # update the global event time object
                event_time.set(event.Time)


if __name__ == '__main__':
    main()
