#!/usr/bin/env python3

import os
import time
import dbus

from typing import Callable, IO

from cortile.helper.dict import Dict
from cortile.base.process import Process


class Session(object):
    def __init__(self, name: str = 'com.github.leukipp.cortile', path: str = '/com/github/leukipp/cortile'):
        """
        Initialize the dbus connector.
        This base class connects to the running cortile instance and communicates
        with the build in cortile dbus client. The results are stored into dictionaries.

        :param name: Dbus name, default is com.github.leukipp.cortile
        :param path: Dbus path, default is /com/github/leukipp/cortile
        """
        self.name = name
        self.path = path
        self.file = str()

    @property
    def connected(self) -> bool:
        """
        Flag that indicates if connect() was successful.

        :return: True if cortile binary exists, False otherwise
        """
        return os.path.exists(self.file)

    def connect(self) -> Dict:
        """
        Retrieve cortile binary path with a direct dbus call.

        :return: Dictionary with success or error data
        """
        try:
            self.file = dbus.SessionBus().get_object(self.name, self.path).Get(self.name, 'Process')['Path']
        except Exception as e:
            return self.data('Error', Message=repr(e))
        return self.data('Result', Success=True)

    def disconnect(self) -> None:
        """
        Disconnect session by resetting cortile binary path.
        """
        self.file = str()

    def listen(self, callback: Callable[[Dict], None], *args: object) -> Process:
        """
        Listen asynchronously to cortile events.

        :param callback: Callback function for cortile action events
        :param args: Optional arguments to filter cortile event types

        :return: Running or empty background process thread
        """
        if not self.connected:
            if callable(callback):
                callback(self.data('Error', Message='Not connected'))
            return Process()
        process = Process(f'{self.file} dbus -listen {" ".join(map(str, args))}')
        process.communicate(lambda a, b, c: callback(self.parse(a, b, c)))
        return process

    def method(self, name: str, *args: object) -> Dict:
        """
        Execute cortile method with arguments.

        :param name: Name of the cortile method
        :param args: Arguments of the cortile method

        :return: Dictionary with success or error data
        """
        if not self.connected:
            return self.data('Error', Message='Not connected')
        process = Process(f'{self.file} dbus -method {name} {" ".join(map(str, args))}')
        return self.parse(*process.communicate())

    def property(self, name: str) -> Dict:
        """
        Retrieve cortile property.

        :param name: Name of the cortile property

        :return: Dictionary with success or error data
        """
        if not self.connected:
            return self.data('Error', Message='Not connected')
        process = Process(f'{self.file} dbus -property {name}')
        return self.parse(*process.communicate())

    def help(self) -> Dict:
        """
        Show the help message from cortile dbus -help.

        :return: Dictionary with success or error data
        """
        if not self.connected:
            return self.data('Error', Message='Not connected')
        process = Process(f'{self.file} dbus -help')
        return self.parse(*process.communicate())

    @staticmethod
    def parse(stdout: IO, stderr: IO, code: int) -> Dict:
        """
        Parse stdout and stderr messages from subprocess.

        :param stdout: Success output of subprocess
        :param stderr: Error output of subprocess
        :param code: Status code of subprocess

        :return: Dictionary with success or error data
        """
        if code:
            return Session.data('Error', Message=stderr.decode('utf-8'))
        return Dict.from_json(stdout.decode('utf-8'))

    @staticmethod
    def data(typ: str, **kwargs: object) -> Dict:
        """
        Create formatted data dict which matches cortile return structure.

        :param typ: Type of the data
        :param kwargs: Keyword arguments of the data

        :return: Dictionary with success or error data
        """
        return Dict(
            Process=os.getpid(),
            Time=int(time.time_ns() / 1e6),
            Type=typ,
            Name='Connector',
            Data=Dict(kwargs)
        )
