#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime


class Waypoint(object):
    def __init__(self, time, latitude, longitude, elevation):
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation

    def __cmp__(self, other):
        if isinstance(other, self.__class__):
            return -1 if self.time < other.time else 0 if self.__eq__(other) else 1
        elif isinstance(other, type(self.time)):
            return -1 if self.time < other.time else 0 if self.time == other.time else 1

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.time < other.time
        elif isinstance(other, type(self.time)):
            return self.time < other

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            return self.time > other.time
        elif isinstance(other, type(self.time)):
            return self.time > other

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (self.time == other.time and
                    self.latitude == other.latitude and
                    self.longitude == other.longitude)
        elif isinstance(other, type(self.time)):
            return self.time == other

if __name__ == "__main__":
    print("Don't run me bro!")
