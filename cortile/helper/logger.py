#!/usr/bin/env python3

import os
import sys
import syslog

from datetime import datetime
from cortile.helper.dict import Dict


class Logger(object):
    LEVELS = Dict(
        DEBUG=0,
        INFO=1,
        WARN=2,
        ERROR=3,
        FATAL=4
    )

    COLORS = Dict(
        RED='\033[31m',
        GREEN='\033[32m',
        BLUE='\033[34m',
        YELLOW='\033[33m',
        MAGENTA='\033[35m',
        CYAN='\033[36m',
        GRAY='\033[37m',
        WHITE='\033[97m',
        BLACK='\033[30m',
        RESET='\033[0m'
    )

    def __init__(self, level=2):
        self.level = level
        self.pid = os.getpid()

    def color(self, level):
        return Dict(
            DEBUG=self.COLORS.GRAY,
            INFO=self.COLORS.CYAN,
            WARN=self.COLORS.YELLOW,
            ERROR=self.COLORS.MAGENTA,
            FATAL=self.COLORS.RED
        )[level]

    def prefix(self, level, colored=True):
        time = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        pid = f'{self.pid}'
        context = f'{level}'
        if colored:
            time = f'{self.COLORS.GRAY}{time}{self.COLORS.RESET}'
            pid = f'{self.COLORS.GRAY}{pid}{self.COLORS.RESET}'
            context = f'{self.color(level)}{context}{self.COLORS.RESET}'
        return f'{time} | {pid} | {context}'

    def log(self, level, text):
        if not (self.LEVELS[level] >= self.level):
            return
        print(f'{self.prefix(level, True)} | {text}')
        syslog.syslog(f'{self.prefix(level, False)} | {text}'.replace('\n', ' '))

    def debug(self, text):
        self.log('DEBUG', text)

    def info(self, text):
        self.log('INFO', text)

    def warn(self, text):
        self.log('WARN', text)

    def error(self, text):
        self.log('ERROR', text)

    def fatal(self, text):
        self.log('FATAL', text)
        sys.exit()
