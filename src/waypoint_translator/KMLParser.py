#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Waypoint

from datetime import datetime
from xml.etree import ElementTree


class KMLParserException(Exception):
    def __init__(self, message):
        super(KMLParserException, self).__init__(message)


class KMLParser(object):
    namespaces = {
        "": "http://www.opengis.net/kml/2.2",
        "gx": "http://www.google.com/kml/ext/2.2"
    }

    def __init__(self, filename):
        self.parser = ElementTree.parse(filename)
        self.document = self.parser.getroot()

    def get_waypoints(self, date_filter=False, older_than=None, newer_than=None):
        tracks = self.document.findall("*//{http://www.google.com/kml/ext/2.2}Track")

        if date_filter and (older_than is None or newer_than is None):
            raise KMLParserException("Error: cannot specify date_filter=True without supplying both older_than "
                                     "and newer_than!")

        for track in tracks:
            children = track.iter()

            current_when = None

            for child in children:
                if child.tag == "{%s}when" % self.namespaces[""]:
                    if current_when is None:
                        try:
                            current_when = datetime.strptime(child.text, "%Y-%m-%dT%H:%M:%SZ")

                            if date_filter and (current_when < older_than or current_when > newer_than):
                                current_when = None
                        except ValueError as e:
                            raise KMLParserException("Error: <when> tag value was in an unexpected format: '%s'"
                                                     % child.text)
                    else:
                        raise KMLParserException("Error: Encountered a second <when> tag before hitting a <gx:coord>!")
                elif child.tag == "{%s}coord" % self.namespaces["gx"]:
                    if current_when is not None:
                        coord = child.text.split(" ")

                        if len(coord) != 3:
                            raise KMLParserException("Error: <gx:coord> tag has too many fields!")

                        try:
                            wp = Waypoint.Waypoint(current_when, float(coord[0]), float(coord[1]), float(coord[2]))

                            yield wp
                        except ValueError:
                            raise KMLParserException("Error: could not parse this <gx:coord> tag [contents: '%s']"
                                                     % child.text)

                        current_when = None
                    # else case: allowed to happen if current_when fell outside of the date range (saves parsing time)

if __name__ == "__main__":
    print("Don't run me bro!")
