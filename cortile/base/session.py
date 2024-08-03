#!/usr/bin/env python3

import os
import time
import dbus

from cortile.helper.dict import Dict
from cortile.base.process import Process


class Session(object):
    def __init__(self, name='com.github.leukipp.cortile', path='/com/github/leukipp/cortile'):
        self.name = name
        self.path = path
        self.file = str()

    @property
    def connected(self):
        return os.path.exists(self.file)

    def connect(self):
        try:
            self.file = dbus.SessionBus().get_object(self.name, self.path).Get(self.name, 'Process')['Path']
        except Exception as e:
            return self.data('Error', Message=repr(e))
        return self.data('Result', Success=True)

    def help(self):
        if not self.connected:
            return self.data('Error', Message='Not connected')
        process = Process(f'{self.file} dbus -help')
        return self.parse(*process.communicate())

    def listen(self, callback, *args):
        if not self.connected:
            callback(self.data('Error', Message='Not connected'))
        process = Process(f'{self.file} dbus -listen {" ".join(map(str, args))}')
        process.communicate(lambda a, b, c: callback(self.parse(a, b, c)))

    def method(self, name, *args):
        if not self.connected:
            return self.data('Error', Message='Not connected')
        process = Process(f'{self.file} dbus -method {name} {" ".join(map(str, args))}')
        return self.parse(*process.communicate())

    def property(self, name):
        if not self.connected:
            return self.data('Error', Message='Not connected')
        process = Process(f'{self.file} dbus -property {name}')
        return self.parse(*process.communicate())

    @staticmethod
    def parse(stdout, stderr, code):
        if code != 1:
            return Session.data('Error', Message=stderr.decode('utf-8'))
        return Dict.from_json(stdout.decode('utf-8'))

    @staticmethod
    def data(typ, **kwargs):
        return Dict(
            Process=os.getpid(),
            Time=int(time.time_ns() / 1e6),
            Type=typ,
            Name='Connector',
            Data=Dict(kwargs)
        )
