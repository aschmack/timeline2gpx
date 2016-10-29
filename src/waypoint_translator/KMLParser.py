#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Waypoint

from datetime import datetime
import io


class KMLParserException(Exception):
    def __init__(self, message):
        super(KMLParserException, self).__init__(message)


class KMLParser(object):
    namespaces = {
        "": "http://www.opengis.net/kml/2.2",
        "gx": "http://www.google.com/kml/ext/2.2"
    }

    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def __enter__(self):
        self.file = io.open(self.filename, "r")
        return self

    def __exit__(self, tp, value, tb):
        if self.file is not None:
            self.file.close()
            self.file = None

    def get_waypoints(self, date_filter=False, older_than=None, newer_than=None):
        if date_filter and (older_than is None or newer_than is None):
            raise KMLParserException("Error: cannot specify date_filter=True without supplying both older_than "
                                     "and newer_than!")

        if self.file is None:
            raise KMLParserException("Error: this class must (at the moment) be used in a with statement!")

        current_when = None

        for full_line in self.file:
            line = full_line.strip(" \t\r\n")

            if line.startswith("<when>"):
                inner_text = line[6:-7]

                if current_when is None:
                    try:
                        current_when = datetime.strptime(inner_text, "%Y-%m-%dT%H:%M:%SZ")

                        if date_filter and (current_when < older_than or current_when > newer_than):
                            current_when = None
                    except ValueError:
                        raise KMLParserException("Error: <when> tag value was in an unexpected format: '%s'"
                                                 % inner_text)
                else:
                    raise KMLParserException("Error: Encountered a second <when> tag before hitting a <gx:coord>!")
            elif line.startswith("<gx:coord>"):
                if current_when is not None:
                    inner_text = line[10:-11]

                    coord = inner_text.split(" ")

                    if len(coord) != 3:
                        raise KMLParserException("Error: <gx:coord> tag has too many fields!")

                    try:
                        wp = Waypoint.Waypoint(current_when, float(coord[1]), float(coord[0]), float(coord[2]))

                        yield wp
                    except ValueError:
                        raise KMLParserException("Error: could not parse this <gx:coord> tag [contents: '%s']"
                                                 % inner_text)

                    current_when = None
                # else case: allowed to happen if current_when fell outside of the date range (saves parsing time)

if __name__ == "__main__":
    print("Don't run me bro!")
