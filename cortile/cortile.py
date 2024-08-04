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

        :param log: Logging level, default is warn
        """
        self.connector = Connector(log)

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
        while not self.connector.exit():
            time.sleep(sleep)

    def get_active_layouts(self) -> Iterator[Dict]:
        """
        Get the active layouts from the workspaces.

        :return: Iterator of active layouts with tiling enabled
        """
        workspaces = self.connector.property('Workspaces')
        for workspace in workspaces.Values if workspaces else []:
            if workspace and workspace.Tiling:
                yield workspace.Layouts[workspace.ActiveLayoutNum]
        return

    def get_active_layout(self) -> Dict | None:
        """
        Get the active layout for the current desk and screen.

        :return: Active layout with tiling enabled or None
        """
        workplace = self.connector.property('Workplace')
        for layout in self.get_active_layouts():
            if not layout or not workplace:
                return None
            if layout.Location.DeskNum == workplace.CurrentDesk and layout.Location.ScreenNum == workplace.CurrentScreen:
                return layout
        return None

    def get_active_client(self) -> Dict | None:
        """
        Get the current focused client window.

        :return: Active client or None
        """
        windows = self.get_windows()
        clients = self.get_clients()
        if not windows or not clients:
            return None
        for client in clients:
            if windows.Active.Id == client.Window.Id:
                return client
        return None

    def get_active_workspace(self) -> int | None:
        """
        Get the current active workspace.

        :return: Active workspace index or None
        """
        workplace = self.connector.property('Workplace')
        if not workplace:
            return None
        return workplace.CurrentDesk

    def get_active_screen(self) -> int | None:
        """
        Get the current active screen.

        :return: Active screen index or None
        """
        workplace = self.connector.property('Workplace')
        if not workplace:
            return None
        return workplace.CurrentScreen

    def get_workspace_count(self) -> int | None:
        """
        Get the number of workspaces.

        :return: Number of workspaces or None
        """
        workplace = self.connector.property('Workplace')
        if not workplace:
            return None
        return workplace.DeskCount

    def get_screen_count(self) -> int | None:
        """
        Get the number of screens.

        :return: Number of screens or None
        """
        workplace = self.connector.property('Workplace')
        if not workplace:
            return None
        return workplace.ScreenCount

    def get_workspace_dimensions(self) -> List[Dict] | None:
        """
        Get the dimensions of all workspaces.

        :return: LTR sorted list of workspace dimensions or None
        """
        workplace = self.connector.property('Workplace')
        if not workplace:
            return None
        return workplace.Displays.Desktops

    def get_screen_dimensions(self) -> List[Dict] | None:
        """
        Get the dimensions of all screens.

        :return: LTR sorted list of screen dimensions or None
        """
        workplace = self.connector.property('Workplace')
        if not workplace:
            return None
        return workplace.Displays.Screens

    def get_windows(self) -> Dict | None:
        """
        Get the windows information.

        :return: List of tracked window ids or None
        """
        windows = self.connector.property('Windows')
        if not windows:
            return None
        return windows

    def get_clients(self) -> List[Dict] | None:
        """
        Get the clients information.

        :return: List of tracked clients or None
        """
        clients = self.connector.property('Clients')
        if not clients:
            return None
        return clients.Values

    def desktop_switch(self, desk: int) -> bool:
        """
        Switch to a different desktop.

        :param desk: Index of the desktop to switch to

        :return: True if successful, False otherwise
        """
        return self.connector.method('DesktopSwitch', desk)

    def window_activate(self, id: int) -> bool:
        """
        Activate a window by its id.

        :param id: Id of the window to activate

        :return: True if successful, False otherwise
        """
        return self.connector.method('WindowActivate', id)

    def window_to_desktop(self, id: int, desk: int) -> bool:
        """
        Move a window to a different desktop.

        :param id: Id of the window to move
        :param desk: Index of the desktop to move the window to

        :return: True if successful, False otherwise
        """
        return self.connector.method('WindowToDesktop', id, desk)

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

    def action_execute_enable(self, desk: int, screen: int) -> bool:
        """
        Execute the 'enable' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'enable', desk, screen)

    def action_execute_disable(self, desk: int, screen: int) -> bool:
        """
        Execute the 'disable' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'disable', desk, screen)

    def action_execute_toggle(self, desk: int, screen: int) -> bool:
        """
        Execute the 'toggle' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'toggle', desk, screen)

    def action_execute_decoration(self, desk: int, screen: int) -> bool:
        """
        Execute the 'decoration' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'decoration', desk, screen)

    def action_execute_restore(self, desk: int, screen: int) -> bool:
        """
        Execute the 'restore' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'restore', desk, screen)

    def action_execute_cycle_next(self, desk: int, screen: int) -> bool:
        """
        Execute the 'cycle_next' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'cycle_next', desk, screen)

    def action_execute_cycle_previous(self, desk: int, screen: int) -> bool:
        """
        Execute the 'cycle_previous' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'cycle_previous', desk, screen)

    def action_execute_layout_vertical_left(self, desk: int, screen: int) -> bool:
        """
        Execute the 'layout_vertical_left' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'layout_vertical_left', desk, screen)

    def action_execute_layout_vertical_right(self, desk: int, screen: int) -> bool:
        """
        Execute the 'layout_vertical_right' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'layout_vertical_right', desk, screen)

    def action_execute_layout_horizontal_top(self, desk: int, screen: int) -> bool:
        """
        Execute the 'layout_horizontal_top' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'layout_horizontal_top', desk, screen)

    def action_execute_layout_horizontal_bottom(self, desk: int, screen: int) -> bool:
        """
        Execute the 'layout_horizontal_bottom' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'layout_horizontal_bottom', desk, screen)

    def action_execute_layout_maximized(self, desk: int, screen: int) -> bool:
        """
        Execute the 'layout_maximized' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'layout_maximized', desk, screen)

    def action_execute_layout_fullscreen(self, desk: int, screen: int) -> bool:
        """
        Execute the 'layout_fullscreen' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'layout_fullscreen', desk, screen)

    def action_execute_master_make(self, desk: int, screen: int) -> bool:
        """
        Execute the 'master_make' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'master_make', desk, screen)

    def action_execute_master_make_next(self, desk: int, screen: int) -> bool:
        """
        Execute the 'master_make_next' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'master_make_next', desk, screen)

    def action_execute_master_make_previous(self, desk: int, screen: int) -> bool:
        """
        Execute the 'master_make_previous' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'master_make_previous', desk, screen)

    def action_execute_master_increase(self, desk: int, screen: int) -> bool:
        """
        Execute the 'master_increase' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'master_increase', desk, screen)

    def action_execute_master_decrease(self, desk: int, screen: int) -> bool:
        """
        Execute the 'master_decrease' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'master_decrease', desk, screen)

    def action_execute_slave_increase(self, desk: int, screen: int) -> bool:
        """
        Execute the 'slave_increase' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'slave_increase', desk, screen)

    def action_execute_slave_decrease(self, desk: int, screen: int) -> bool:
        """
        Execute the 'slave_decrease' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'slave_decrease', desk, screen)

    def action_execute_proportion_increase(self, desk: int, screen: int) -> bool:
        """
        Execute the 'proportion_increase' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'proportion_increase', desk, screen)

    def action_execute_proportion_decrease(self, desk: int, screen: int) -> bool:
        """
        Execute the 'proportion_decrease' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'proportion_decrease', desk, screen)

    def action_execute_window_next(self, desk: int, screen: int) -> bool:
        """
        Execute the 'window_next' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'window_next', desk, screen)

    def action_execute_window_previous(self, desk: int, screen: int) -> bool:
        """
        Execute the 'window_previous' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'window_previous', desk, screen)

    def action_execute_reset(self, desk: int, screen: int) -> bool:
        """
        Execute the 'reset' action.

        :param desk: Index of the desktop
        :param screen: Index of the screen

        :return: True if successful, False otherwise
        """
        return self.connector.method('ActionExecute', 'reset', desk, screen)
