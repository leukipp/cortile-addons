#!/usr/bin/env python3

from datetime import datetime, timezone, timedelta


class Time(object):
    def __init__(self, ts: int = 0.0, tz: timezone = timezone.utc):
        """
        Initialize the time helper.
        This helper class converts unix timestamps in milliseconds into datetime objects.
        Additionally, it can calculate the time difference relative to the current moment.

        :param ts: Initial unix timestamp in milliseconds, default is 0.0
        :param tz: Optional datetime timezone, default is utc
        """
        self.tz = tz
        self.dt = datetime.fromtimestamp(ts / 1000.0, tz=self.tz)

    def get(self) -> datetime:
        """
        Get datetime object from stored time.

        :return: Datetime object obtained from timestamp
        """
        return self.dt

    def set(self, ts: int) -> None:
        """
        Set datetime object from unix timestamp.

        :param ts: Unix timestamps in milliseconds
        """
        self.dt = datetime.fromtimestamp(ts / 1000.0, tz=self.tz)

    def now(self) -> datetime:
        """
        Get datetime object with current time.

        :return: Datetime object of now
        """
        return datetime.now(tz=self.tz)

    def delta(self) -> timedelta:
        """
        Get time difference to the stored datetime object.

        :return: Timedelta between now and stored time
        """
        return self.now() - self.dt
