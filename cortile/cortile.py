#!/usr/bin/env python3

import time

from cortile.helper.logger import Logger
from cortile.base.connector import Connector


class Cortile(object):
    def __init__(self, log=Logger.LEVELS.DEBUG):
        self.connector = Connector(log)

    def listen(self, callback):
        self.connector.listen(callback)

    def wait(self, sleep=1.0):
        while not self.connector.exit():
            time.sleep(sleep)

    def get_active_button(self):
        pointer = self.connector.property('Pointer')
        if pointer is None:
            return None
        return pointer.Device

    def get_active_client(self):
        clients = self.connector.property('Clients')
        windows = self.connector.property('Windows')
        if windows is None or clients is None:
            return None
        for client in clients.Values:
            if windows.Active.Id == client.Window.Id:
                return client
        return None

    def get_active_layout(self):
        workplace = self.connector.property('Workplace')
        if workplace is None:
            return None
        for layout in self.get_active_layouts():
            if layout is None:
                return None
            if layout.Location.DeskNum == workplace.CurrentDesk and layout.Location.ScreenNum == workplace.CurrentScreen:
                return layout
        return None

    def get_active_layouts(self):
        workspaces = self.connector.property('Workspaces')
        if workspaces is None:
            yield None
        for workspace in workspaces.Values:
            yield workspace.Layouts[workspace.ActiveLayoutNum]
        yield None
