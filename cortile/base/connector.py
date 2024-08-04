#!/usr/bin/env python3

from typing import Callable

from cortile.helper.dict import Dict
from cortile.helper.logger import Logger
from cortile.helper.signal import Signal
from cortile.base.session import Session


class Connector(object):
    def __init__(self, log: int = Logger.LEVELS.WARN):
        self.log = Logger(log)

        self.properties = Dict()
        self.listener = [self.update]

        self.signal = Signal()
        self.session = Session()

        ret = self.session.connect()
        if ret.Type == 'Result' and ret.Data.Success:
            self.log.info('Init: Connection established')
        if ret.Type == 'Error':
            self.log.fatal(f'Error: {ret.Data.Message}')
        self.session.listen(self.callbacks)

    def exit(self) -> bool:
        return self.signal.exit

    def connected(self) -> bool:
        return self.session.connected

    def help(self) -> str:
        return self.session.help().Data.Message

    def listen(self, callback: Callable[[Dict], None] | None) -> None:
        if not callable(callback):
            return
        self.listener.append(callback)

    def method(self, name: str, *args: object) -> bool:
        self.log.info(f'Method: {name} {" ".join(map(str, args))}')
        ret = self.session.method(name, *args)
        if ret.Type == 'Error':
            self.log.error(f'Error: {ret.Data.Message}')
        return ret.Type == 'Result' and ret.Data.Success

    def property(self, name: str, cached: bool = True) -> Dict | None:
        self.log.info(f'Property: {name}')
        if name not in self.properties or not cached:
            ret = self.session.property(name)
            if ret.Type == 'Error':
                self.log.error(f'Error: {ret.Data.Message}')
            if ret.Type == 'Property':
                self.properties[name] = ret.Data
        return self.properties[name] if name in self.properties else None

    def update(self, ret: Dict | None) -> None:
        if ret is None or ret.Type != 'Property':
            return
        self.log.info(f'{ret.Type}: {ret.Name} update')
        self.properties[ret.Name] = ret.Data

    def callbacks(self, ret: Dict | None) -> None:
        for callback in self.listener:
            callback(ret)
