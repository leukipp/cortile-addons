#!/usr/bin/env python3

import time

from typing import Callable, Iterator, List

from cortile.helper.dict import Dict
from cortile.helper.logger import Logger
from cortile.base.connector import Connector


class Cortile(object):
    def __init__(self, log: int = Logger.LEVELS.WARN):
        """
        Initialize the cortile connector.
        This main class wraps methods of the base connector and should be
        used as primary interface to communicate with a running cortile instance.

        :param log: Logging level, default is warn
        """
        self.connector = Connector(log)

    @property
    def log(self) -> Logger:
        """
        Return the logger instance.

        :return: Logger instance that writes to syslog
        """
        return self.connector.log

    def listen(self, callback: Callable[[Dict], None] | None) -> None:
        """
        Start listening for events.

        :param callback: Function to call when an event is received
        """
        self.connector.listen(callback)

    def wait(self, sleep: float = 0.5) -> None:
        """
        Keeps the process running for the connector to listen.

        :param sleep: Time to sleep in between, default is 0.5 seconds
        """
        while self.connector.connected and not self.connector.exit:
            time.sleep(sleep)
        self.close()

    def close(self) -> None:
        """
        Close the connection gracefully.
        """
        self.connector.close()

    def get_active_layout(self) -> Dict | None:
        """
        Get the active layout for the current desktop and screen.

        :return: Active layout with tiling enabled or None
        """
        workplace = self.connector.property('Workplace')
        if not workplace:
            return None
        for layout in self.get_active_layouts():
            if layout.Location.Desktop == workplace.CurrentDesktop and layout.Location.Screen == workplace.CurrentScreen:
                return layout
        return None

    def get_active_layouts(self) -> Iterator[Dict]:
        """
        Get the active layouts from the workspaces.

        :return: Iterator of active layouts with tiling enabled
        """
        workspaces = self.connector.property('Workspaces')
        if not workspaces:
            return
        for workspace in workspaces.Values:
            if workspace.Tiling:
                yield workspace.Layouts[workspace.Layout]
        return

    def get_active_client(self) -> Dict | None:
        """
        Get the current focused client window.

        :return: Active client or None
        """
        clients = self.get_clients()
        windows = self.get_windows()
        for client in clients:
            if windows and windows.Active.Id == client.Window.Id:
                return client
        return None

    def get_active_clients(self) -> Iterator[Dict]:
        """
        Get information of clients on the current active screen.

        :return: Iterator of tracked clients on the current screen
        """
        clients = self.connector.property('Clients')
        workplace = self.connector.property('Workplace')
        if not clients or not workplace:
            return
        for client in clients.Values:
            location = client.Latest.Location
            if location.Desktop == workplace.CurrentDesktop and location.Screen == workplace.CurrentScreen:
                yield client
        return

    def get_active_desktop(self) -> int | None:
        """
        Get the current active desktop.

        :return: Active desktop index or None
        """
        workplace = self.connector.property('Workplace')
        if not workplace:
            return None
        return workplace.CurrentDesktop

    def get_active_screen(self) -> int | None:
        """
        Get the current active screen.

        :return: Active screen index or None
        """
        workplace = self.connector.property('Workplace')
        if not workplace:
            return None
        return workplace.CurrentScreen

    def get_desktop_count(self) -> int | None:
        """
        Get the number of desktops.

        :return: Number of desktops or None
        """
        workplace = self.connector.property('Workplace')
        if not workplace:
            return None
        return workplace.DesktopCount

    def get_screen_count(self) -> int | None:
        """
        Get the number of screens.

        :return: Number of screens or None
        """
        workplace = self.connector.property('Workplace')
        if not workplace:
            return None
        return workplace.ScreenCount

    def get_desktop_dimensions(self) -> List[Dict]:
        """
        Get the dimensions of all desktops.

        :return: LTR sorted list of desktop dimensions or None
        """
        workplace = self.connector.property('Workplace')
        if not workplace:
            return []
        return workplace.Displays.Desktops

    def get_screen_dimensions(self) -> List[Dict]:
        """
        Get the dimensions of all screens.

        :return: LTR sorted list of screen dimensions or None
        """
        workplace = self.connector.property('Workplace')
        if not workplace:
            return []
        return workplace.Displays.Screens

    def get_clients(self) -> List[Dict]:
        """
        Get all the clients information.

        :return: List of tracked clients or None
        """
        clients = self.connector.property('Clients')
        if not clients:
            return []
        return clients.Values

    def get_windows(self) -> Dict | None:
        """
        Get all the windows information.

        :return: List of tracked window ids or None
        """
        windows = self.connector.property('Windows')
        if not windows:
            return None
        return windows

    def desktop_switch(self, desktop: int) -> bool:
        """
        Switch to a different desktop.

        :param desktop: Index of the desktop to switch to

        :return: True if successful, False otherwise
        """
        return self.connector.method('DesktopSwitch', desktop)

    def window_activate(self, id: int) -> bool:
        """
        Activate a window by its id.

        :param id: Id of the window to activate

        :return: True if successful, False otherwise
        """
        return self.connector.method('WindowActivate', id)

    def window_to_desktop(self, id: int, desktop: int) -> bool:
        """
        Move a window to a different desktop.

        :param id: Id of the window to move
        :param desktop: Index of the desktop to move the window to

        :return: True if successful, False otherwise
        """
        return self.connector.method('WindowToDesktop', id, desktop)

    def window_to_position(self, id: int, x: int, y: int) -> bool:
        """
        Move a window to a specific position.

        :param id: Id of the window to move
        :param x: X coordinate to move the window to
        :param y: Y coordinate to move the window to

        :return: True if successful, False otherwise
        """
        return self.connector.method('WindowToPosition', id, x, y)

    def window_to_screen(self, id: int, screen: int) -> bool:
        """
        Move a window to a different screen.

        :param id: Id of the window to move
        :param screen: Index of the screen to move the window to

        :return: True if successful, False otherwise
        """
        return self.connector.method('WindowToScreen', id, screen)

    def action_execute_enable(self, desktop: int, screen: int) -> bool:
        """
        Execute the `enable` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'enable', desktop, screen)

    def action_execute_disable(self, desktop: int, screen: int) -> bool:
        """
        Execute the `disable` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'disable', desktop, screen)

    def action_execute_toggle(self, desktop: int, screen: int) -> bool:
        """
        Execute the `toggle` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'toggle', desktop, screen)

    def action_execute_decoration(self, desktop: int, screen: int) -> bool:
        """
        Execute the `decoration` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'decoration', desktop, screen)

    def action_execute_restore(self, desktop: int, screen: int) -> bool:
        """
        Execute the `restore` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'restore', desktop, screen)

    def action_execute_reset(self, desktop: int, screen: int) -> bool:
        """
        Execute the `reset` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'reset', desktop, screen)

    def action_execute_cycle_next(self, desktop: int, screen: int) -> bool:
        """
        Execute the `cycle_next` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'cycle_next', desktop, screen)

    def action_execute_cycle_previous(self, desktop: int, screen: int) -> bool:
        """
        Execute the `cycle_previous` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'cycle_previous', desktop, screen)

    def action_execute_layout_vertical_left(self, desktop: int, screen: int) -> bool:
        """
        Execute the `layout_vertical_left` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'layout_vertical_left', desktop, screen)

    def action_execute_layout_vertical_right(self, desktop: int, screen: int) -> bool:
        """
        Execute the `layout_vertical_right` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'layout_vertical_right', desktop, screen)

    def action_execute_layout_horizontal_top(self, desktop: int, screen: int) -> bool:
        """
        Execute the `layout_horizontal_top` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'layout_horizontal_top', desktop, screen)

    def action_execute_layout_horizontal_bottom(self, desktop: int, screen: int) -> bool:
        """
        Execute the `layout_horizontal_bottom` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'layout_horizontal_bottom', desktop, screen)

    def action_execute_layout_maximized(self, desktop: int, screen: int) -> bool:
        """
        Execute the `layout_maximized` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'layout_maximized', desktop, screen)

    def action_execute_layout_fullscreen(self, desktop: int, screen: int) -> bool:
        """
        Execute the `layout_fullscreen` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'layout_fullscreen', desktop, screen)

    def action_execute_slave_increase(self, desktop: int, screen: int) -> bool:
        """
        Execute the `slave_increase` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'slave_increase', desktop, screen)

    def action_execute_slave_decrease(self, desktop: int, screen: int) -> bool:
        """
        Execute the `slave_decrease` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'slave_decrease', desktop, screen)

    def action_execute_master_increase(self, desktop: int, screen: int) -> bool:
        """
        Execute the `master_increase` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'master_increase', desktop, screen)

    def action_execute_master_decrease(self, desktop: int, screen: int) -> bool:
        """
        Execute the `master_decrease` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'master_decrease', desktop, screen)

    def action_execute_window_next(self, desktop: int, screen: int) -> bool:
        """
        Execute the `window_next` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'window_next', desktop, screen)

    def action_execute_window_previous(self, desktop: int, screen: int) -> bool:
        """
        Execute the `window_previous` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'window_previous', desktop, screen)

    def action_execute_screen_next(self, desktop: int, screen: int) -> bool:
        """
        Execute the `screen_next` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'screen_next', desktop, screen)

    def action_execute_screen_previous(self, desktop: int, screen: int) -> bool:
        """
        Execute the `screen_previous` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'screen_previous', desktop, screen)

    def action_execute_master_make(self, desktop: int, screen: int) -> bool:
        """
        Execute the `master_make` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'master_make', desktop, screen)

    def action_execute_master_make_next(self, desktop: int, screen: int) -> bool:
        """
        Execute the `master_make_next` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'master_make_next', desktop, screen)

    def action_execute_master_make_previous(self, desktop: int, screen: int) -> bool:
        """
        Execute the `master_make_previous` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'master_make_previous', desktop, screen)

    def action_execute_proportion_increase(self, desktop: int, screen: int) -> bool:
        """
        Execute the `proportion_increase` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'proportion_increase', desktop, screen)

    def action_execute_proportion_decrease(self, desktop: int, screen: int) -> bool:
        """
        Execute the `proportion_decrease` action.

        :param desktop: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'proportion_decrease', desktop, screen)
