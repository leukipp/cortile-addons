#!/usr/bin/env python3

import threading
import subprocess

from typing import Callable, Tuple, IO


class Process(threading.Thread):
    def __init__(self, command: str = None, daemon: bool = True):
        """
        Initialize the process thread.
        This base class runs a subprocess in a background thread and returns
        stdout and stderr, either synchronously or asynchronously using callbacks.

        :param command: Command string of the process, default is None
        :param daemon: Run thread as daemon, default is True
        """
        super().__init__(daemon=daemon)
        self.process = None
        self.callback = None
        self.init(command)

    def init(self, command: str | None, shell: bool = True) -> None:
        """
        Instantiate a subprocess child program.

        :param command: Command string of the process, default is None
        :param shell: Run subprocess as shell command, default is True
        """
        if not isinstance(command, str):
            return
        self.process = subprocess.Popen([command], shell=shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def run(self) -> None:
        """
        Run the subprocess and send stdout to callback.
        """
        if not isinstance(self.process, subprocess.Popen):
            return
        while callable(self.callback) and self.process.poll() is None:
            stdout = self.process.stdout.readline()
            if len(stdout) == 0:
                continue
            self.callback(stdout, b'', 0)

    def communicate(self, callback: Callable[[IO, IO, int], None] | None = None) -> Tuple[IO, IO, int] | None:
        """
        Communicate synchronous or asynchronous with subprocess.

        :param callback: Optional callback function for asynchronous calls
        """
        if not isinstance(self.process, subprocess.Popen):
            return
        if not callable(callback):
            return *self.process.communicate(), self.process.poll()
        self.callback = callback
        self.start()

    def terminate(self) -> None:
        """
        Terminate the subprocess thread gracefully.
        """
        if not isinstance(self.process, subprocess.Popen):
            return
        self.process.terminate()
