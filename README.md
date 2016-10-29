#timeline2gpx - Translate KML into GPX
***
This tool was designed to parse the KML files output from Google's Timeline feature and translate them, with timestamps, into GPX files which can be read in Lightroom.

## Usage

timeline2gpx.py [options] <KML file>...
   --or--
timeline2gpx.exe [options] <KML file>...
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