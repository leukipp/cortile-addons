#!/usr/bin/env python3

"""Export the current tiling state into files.

This example listens to cortile events and handles workspace updates.
It retrieves the current layouts and exports tiling states and decoration
states for each screen and desktop into files. The export folder path is
hardcoded [see TODO]. This script serves as an example of how to retrieve
properties from active layouts and to use it afterward for custom logic.

Authors:
    * https://github.com/leukipp/

Dependencies:
    The following packages have to be installed::

        $ pip install cortile

Usage:
    Run the python application::

        $ python write_tiling_state_file.py

"""


import os
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

    # the callback will fire on all events, here we are only interested on workspace updates
    if event.Name == 'Workspaces':
        handle_workspace_update(ct)


def handle_workspace_update(ct: Cortile):

    # TODO: adjust export folder path
    export_folder = os.path.join(os.path.sep, 'tmp', 'cortile')

    # create folder structure
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    # dictionary that stores a mapping between file path and file contents
    files = Dict()

    # initialize dictionary with default values, key is file path and value the "active_layout_name;decoration_state"
    for screen_index in range(ct.get_screen_count()):
        for workspace_index in range(ct.get_workspace_count()):
            file_name = f'screen{screen_index}-desktop{workspace_index}.txt'
            file_path = os.path.join(export_folder, file_name)

            # initialize files dictionary
            files[file_path] = 'disabled;None'

    # update dictionary with actual values, get_active_layouts() only returns layouts with tiling enabled
    for layout in ct.get_active_layouts():
        file_name = f'screen{layout.Location.Screen}-desktop{layout.Location.Desktop}.txt'
        file_path = os.path.join(export_folder, file_name)

        # update files dictionary
        files[file_path] = f'{layout.Name};{layout.Decoration}'

    # export state files
    export_state_files(files)


def export_state_files(files: Dict):
    print(f'Export files: {files}')

    # iterate over the dictionary and write states to the file system
    for file_path, file_content in files.items():
        with open(file_path, 'w') as file:
            file.write(file_content)


if __name__ == '__main__':
    main()
