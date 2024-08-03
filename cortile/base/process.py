#!/usr/bin/env python3

import threading
import subprocess


class Process(threading.Thread):
    def __init__(self, command):
        super().__init__()
        self.callback = None
        self.process = subprocess.Popen([command], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def communicate(self, callback=None):
        if callback is None:
            return *self.process.communicate(), self.process.poll()
        self.callback = callback
        self.start()

    def run(self):
        while self.callback != None and self.process.poll() is None:
            stdout = self.process.stdout.readline()
            if len(stdout) == 0:
                continue
            self.callback(stdout, b'', 1)
