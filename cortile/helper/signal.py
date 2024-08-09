#!/usr/bin/env python3

import sys
import signal

from types import FrameType


class Signal(object):
    def __init__(self):
        """
        Initialize the signal handler.
        This helper class manages sigint and sigterm events to signal whether
        an application exit has been requested, ensuring a gracefully termination.
        """
        self.sigcount = 0
        signal.signal(signal.SIGINT, self.sig)
        signal.signal(signal.SIGTERM, self.sig)

    def sig(self, number: int, frame: FrameType) -> None:
        """
        Handle signal events.

        :param number: Signal number, not used
        :param frame: Signal frame, not used
        """
        self.sigcount += 1
        if self.sigcount > 2:
            sys.exit(0)

    @property
    def exit(self) -> bool:
        """
        Flag that indicates if sig() event was triggered.

        :return: True if sig event was triggered, False otherwise
        """
        return self.sigcount > 0
