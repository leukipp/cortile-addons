#!/usr/bin/env python3

from typing import Callable, Tuple

from cortile.helper.dict import Dict
from cortile.helper.logger import Logger
from cortile.helper.signal import Signal
from cortile.base.session import Session


class Connector(object):
    def __init__(self, log: int = Logger.LEVELS.WARN):
        """
        Initialize the session connector.
        This base class acts as a middle layer and wraps session methods for
        registration of listener callbacks and caching of received cortile properties.

        :param log: Logging level, default is warn
        """
        self.log = Logger(log)
        self.signal = Signal()
        self.session = Session()
        self.properties = Dict()
        self.listener = [self.observe]
        result = self.session.connect()
        if result.Type == 'Result' and result.Data.Success:
            self.log.info('Init: Connection established')
        if result.Type == 'Error':
            self.log.fatal(f'Error: {result.Data.Message}')
        self.process = self.session.listen(self.callbacks)

    @property
    def connected(self) -> bool:
        """
        Flag that indicates if session.connect() was successful.

        :return: True if cortile binary is running, False otherwise
        """
        return self.process.running and self.session.connected

    @property
    def exit(self) -> bool:
        """
        Flag that indicates if signal.sig() event was triggered.

        :return: True if sig event was triggered, False otherwise
        """
        return self.signal.exit

    def close(self) -> None:
        """
        Close the connection gracefully.
        """
        self.log.info(f'Close connection: {self.session.file}')
        self.session.disconnect()
        self.process.terminate()

    def listen(self, callback: Callable[[Dict], None]) -> None:
        """
        Listen asynchronously to cortile events.

        :param callback: Callback function for cortile action events
        """
        self.log.info(f'Register listener: {len(self.listener)}')
        self.listener.append(callback)

    def method(self, name: str, *args: Tuple[str, ...]) -> bool:
        """
        Execute cortile method with arguments.

        :param name: Name of the cortile method
        :param args: Arguments of the cortile method

        :return: True if successful, False otherwise
        """
        self.log.info(f'Method: {name} {" ".join(map(str, args))}')
        result = self.session.method(name, *args)
        if result.Type == 'Error':
            self.log.error(f'Error: {result.Data.Message}')
        return result.Type == 'Result' and result.Data.Success

    def property(self, name: str, cached: bool = True) -> Dict | None:
        """
        Retrieve cortile property.

        :param name: Name of the cortile property
        :param cached: Use the cached value from internal listener, default is True

        :return: Dictionary with success data or None
        """
        self.log.info(f'Property: {name}')
        if name not in self.properties or not cached:
            result = self.session.property(name)
            if result.Type == 'Error':
                self.log.error(f'Error: {result.Data.Message}')
            if result.Type == 'Property':
                self.properties[name] = result.Data
        return self.properties[name] if name in self.properties else None

    def help(self) -> str:
        """
        Show the help message from cortile dbus -help.

        :return: String with help message output
        """
        return self.session.help().Data.Message

    def observe(self, result: Dict | None) -> None:
        """
        Internal function to update cached properties or disconnect client.

        :param result: Dictionary with success or error data
        """
        if not result or result.Type != 'Property':
            return
        if result.Name == 'Disconnect':
            return self.close()
        self.log.info(f'{result.Type}: {result.Name} update')
        self.properties[result.Name] = result.Data

    def callbacks(self, result: Dict | None) -> None:
        """
        Internal function to execute registered callback functions.

        :param result: Dictionary with success or error data
        """
        if not result:
            return
        for callback in self.listener:
            if not callable(callback):
                continue
            callback(result)
