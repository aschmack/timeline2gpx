#!/usr/bin/env python
# -*- coding: utf-8 -*-


class WriterException(Exception):
    def __init__(self, message):
        super(WriterException, self).__init__(message)


class Writer(object):
    def __init__(self):
        pass

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, type, value, tb):
        raise NotImplementedError

    def write_waypoint(self, waypoint):
        raise NotImplementedError

if __name__ == "__main__":
    print("Don't run me bro!")
