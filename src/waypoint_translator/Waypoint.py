#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from functools import total_ordering


@total_ordering
class Waypoint(object):
    def __init__(self, time, latitude, longitude, elevation):
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation

    def __lt__(self, other):
        if type(other) == self.__class__:
            return self.time < other.time
        elif type(other) == datetime.__class__:
            return self.time < other

    def __gt__(self, other):
        if type(other) == self.__class__:
            return self.time > other.time
        elif type(other) == datetime.__class__:
            return self.time > other

    def __eq__(self, other):
        if type(other) == self.__class__:
            return (self.time == other.time and
                    self.latitude == other.latitude and
                    self.longitude == other.longitude)
        elif type(other) == datetime.__class__:
            return self.time == other

if __name__ == "__main__":
    print("Don't run me bro!")
