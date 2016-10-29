#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Waypoint
import Writer

from datetime import datetime
import os
from xml.dom import minidom
from xml.dom import Node
from xml.dom.minidom import Document
from xml.dom.minidom import Element


class GPXWriterException(Writer.WriterException):
    def __init__(self, message):
        super(GPXWriterException, self).__init__(message)


class GPXWriter(Writer.Writer):
    doc_attributes = {
        "xmlns": "http://www.topografix.com/GPX/1/1",
        "xmlns:gpxx": "http://www.garmin.com/xmlschemas/GpxExtensions/v3",
        "xmlns:gpxtpx": "http://www.garmin.com/xmlschemas/TrackPointExtension/v1",
        "creator": "timeline2gpx; github.com/aschmack/timeline2gpx",
        "version": "1.1",
        "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "xsi:schemaLocation": "http://www.topografix.com/GPX/1/1 "
                              "http://www.topografix.com/GPX/1/1/gpx.xsd "
                              "http://www.garmin.com/xmlschemas/GpxExtensions/v3 "
                              "http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd "
                              "http://www.garmin.com/xmlschemas/TrackPointExtension/v1 "
                              "http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd"
    }

    doc_metadata_link = "https://github.com/aschmack/timeline2gpx"
    doc_metadata_text = "Created with timeline2gpx"

    def __init__(self, output_dir, max_count):
        self.output_dir = output_dir
        self.max_count = max_count

        self.current_doc = None
        self.current_trkseg = None
        self.current_time = None

        self.current_count = 0
        self.min_date = None
        self.max_date = None

    def __enter__(self):
        return self

    def __exit__(self, tp, value, tb):
        if self.current_doc is not None:
            self._finish_doc()

    def write_waypoint(self, waypoint):
        if self.current_doc is None:
            self._start_doc()

        # Create new elements
        trkpt_el = self.current_doc.createElement("trkpt")
        ele_el = self.current_doc.createElement("ele")
        time_el = self.current_doc.createElement("time")

        # Set their contents/attributes
        trkpt_el.setAttribute("lat", "%.08f" % waypoint.latitude)
        trkpt_el.setAttribute("lon", "%.08f" % waypoint.longitude)

        ele_el.appendChild(self.current_doc.createTextNode("%d" % waypoint.elevation))

        time_el.appendChild(self.current_doc.createTextNode(waypoint.time.strftime("%Y-%m-%dT%H:%M:%SZ")))

        # Add everything to the tree
        trkpt_el.appendChild(ele_el)
        trkpt_el.appendChild(time_el)
        self.current_trkseg.appendChild(trkpt_el)

        # Accounting
        self.current_count += 1
        if self.min_date is None or waypoint < self.min_date:
            self.min_date = waypoint.time

        if self.max_date is None or waypoint > self.max_date:
            self.max_date = waypoint.time

        if self.current_count >= self.max_count:
            self._finish_doc()

    def _start_doc(self):
        if self.current_doc is not None:
            raise GPXWriterException("Error: tried to create a new document while one already exists!")

        self.current_doc = minidom.getDOMImplementation().createDocument(None, "gpx", None)
        doc_el = self.current_doc.documentElement

        for key, val in self.doc_attributes.iteritems():
            doc_el.setAttribute(key, val)

        meta_el = self.current_doc.createElement("metadata")
        doc_el.appendChild(meta_el)

        link_el = self.current_doc.createElement("link")
        link_el.setAttribute("href", self.doc_metadata_link)
        link_el.appendChild(self.current_doc.createTextNode(self.doc_metadata_text))
        meta_el.appendChild(link_el)

        self.current_time = self.current_doc.createElement("time")
        meta_el.appendChild(self.current_time)

        trk_el = self.current_doc.createElement("trk")
        doc_el.appendChild(trk_el)

        name_el = self.current_doc.createElement("name")
        name_el.appendChild(self.current_doc.createTextNode("Google Maps Timeline Track"))
        trk_el.appendChild(name_el)

        self.current_trkseg = self.current_doc.createElement("trkseg")
        trk_el.appendChild(self.current_trkseg)

    def _finish_doc(self):
        if self.current_doc is None:
            return

        self.current_time.appendChild(self.current_doc.createTextNode(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")))

        count = 1

        while True:
            filename = os.path.join(self.output_dir,
                                    "timeline_%s_%s%s.gpx" %
                                    (self.min_date.strftime("%Y-%m-%d"), self.max_date.strftime("%Y-%m-%d"),
                                     "_%d" % count if count != 1 else ""))
            if not os.path.exists(filename):
                break
            else:
                count += 1

        with open(filename, "w+") as output_file:
            self.current_doc.writexml(output_file, encoding="UTF-8")

        print("Wrote %d waypoints to %s!" % (self.current_count, filename))

        self._reset_current()

    def _reset_current(self):
        self.current_doc.unlink()

        self.current_doc = None
        self.current_trkseg = None
        self.current_time = None

        self.current_count = 0
        self.min_date = None
        self.max_date = None

if __name__ == "__main__":
    print("Don't run me bro!")
