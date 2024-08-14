#!/usr/bin/env python3

import subprocess

from threading import Thread, Event
from typing import Callable, Tuple, IO


class Process(Thread):
    def __init__(self, *args: Tuple[str, ...]):
        """
        Initialize the process thread.
        This base class runs a subprocess in a background thread and returns
        stdout and stderr, either synchronously or asynchronously using callbacks.

        :param args: Process binary path and arguments
        """
        super().__init__(daemon=True)
        self.process = None
        self.callback = None
        self.open = Event()
        if len(args):
            self.process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.open.set()

    @property
    def running(self) -> bool:
        """
        Flag that indicates if subprocess is still running.

        :return: True if subprocess is running, False otherwise
        """
        return self.open.is_set()

    def run(self) -> None:
        """
        Run the subprocess and send stdout to callback.
        """
        if not isinstance(self.process, subprocess.Popen):
            return
        while callable(self.callback) and self.process.poll() is None:
            try:
                stdout = self.process.stdout.readline()
                if stdout is None or len(stdout) == 0:
                    continue
                self.callback(stdout, b'', 0)
            except Exception as e:
                break
        self.open.clear()

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
