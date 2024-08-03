#!/usr/bin/env python3

import sys
import signal


class Signal(object):
    def __init__(self):
        self.sigcount = 0
        signal.signal(signal.SIGINT, self.sig)
        signal.signal(signal.SIGTERM, self.sig)

    def sig(self, num, frame):
        self.sigcount += 1
        if self.sigcount > 2:
            sys.exit(0)

    @property
    def exit(self):
        return self.sigcount > 0
