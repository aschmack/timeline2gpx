#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""timeline2gpx.py: Parse a timeline KML file from Google to generate GPX files
                    for import into Lightroom (or other things, I don't care!)"""


from waypoint_translator import *

from datetime import datetime
import getopt
import os
import sys

__author__      = "aschmack"
__copyright__   = "Copyright 2016"
__license__     = "MIT"
__version__     = "0.1"
__maintainer__  = "You"
__status__      = "Development"

USAGE = """%s [options] <KML file>...
    Parse one or more timeline KML files exported from Google and outputs a standard GPX file
    for import into Lightroom or other tools.

    The exported files will be named 'timeline-<from date>-<to date>.gpx'

    Options
        -f <date>, --from <date>            Only include points later than this parameter. Should
                                            be formatted as YYYY-MM-DD.
        -t <date>, --to <date>              Only include points earlier than this parameter. Should
                                            also be formatted as YYYY-MM-DD.
        --output-dir <directory>            Choose a custom directory in which the generated GPX files
                                            will be placed. Defaults to the current directory. Directory
                                            must exist beforehand.
        -m <int>, --max-points <int>        Set the maximum number of points to output per file. Defaults
                                            to 100000.
"""

DEFAULT_SETTINGS = {
    "from": "1970-01-01",
    "to": "2100-12-31",
    "max_per_file": 100000,
    "output_dir": "."
}


def main(argv):
    config, paths = parse_args(argv)

    if not validate_config(config) or not validate_paths(paths):
        print(USAGE % argv[0])
        return 1

    filtering_dates = (config["from"].year != 1970 or
                       config["to"].year != 2100)

    with GPXWriter.GPXWriter(config["output_dir"], config["max_per_file"]) as writer:
        for path in paths:
            with KMLParser.KMLParser(path) as reader:
                for wp in reader.get_waypoints(filtering_dates, config["from"], config["to"]):
                    writer.write_waypoint(wp)

    print("All done!")


def parse_args(argv):
    config = DEFAULT_SETTINGS.copy()

    try:
        opts, args = getopt.getopt(argv[1:], 'f:t:m:h?',
                                   ["from=", "to=", "output-dir", "max-points", "help"])
    except getopt.GetoptError:
        return {}, []

    for o, a in opts:
        if o in ("-f", "--from"):
            config["from"] = a
        elif o in ("-t", "--to"):
            config["to"] = a
        elif o in ("-m", "--max-points"):
            try:
                config["max_per_file"] = int(a)
            except ValueError:
                print("Error: value given for %s is not a valid integer (%s)!" % (o, a))
                return {}, []
        elif o == "--output-dir":
            config["output_dir"] = a
        elif o in ("-h", "--help", "-?"):
            return {}, []

    return config, args


def validate_config(config):
    is_valid = True

    if len(config.keys()) == 0:
        return False

    try:
        config["from"] = datetime.strptime(config["from"], "%Y-%m-%d")
    except ValueError:
        print("Error: value given for -f or --from does not match the expected format.")
        is_valid = False

    try:
        config["to"] = datetime.strptime(config["to"], "%Y-%m-%d")
    except ValueError:
        print("Error: value given for -t or --to does not match the expected format.")
        is_valid = False

    if not os.path.exists(config["output_dir"]) or not os.path.isdir(config["output_dir"]):
        print("Error: value given for --output_dir does not exist or is not a directory.")
        is_valid = False

    return is_valid


def validate_paths(paths):
    is_valid = True

    if len(paths) == 0:
        print("Error: no files given for conversion!")
        is_valid = False

    for path in paths:
        if not os.path.exists(path):
            print("Error: File '%s' does not exist!" % path)
            is_valid = False

    return is_valid


if __name__ == "__main__":
    sys.exit(main(sys.argv))
