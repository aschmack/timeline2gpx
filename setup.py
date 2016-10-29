# Package it up into an exe to make it easier for people


from distutils.core import setup
import py2exe
import sys

sys.path.append("src")

# If run without args, build executables, in quiet mode.
if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-q")

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources
        self.version = "0.1"
        self.company_name = "aschmack"
        self.copyright = "MIT"
        self.name = "timeline2gpx"

console_app = Target(
    description = "Transform KML files into GPX files",
    script = "src/timeline2gpx.py",
    dest_base = "timeline2gpx"
)

setup(
    options = { "py2exe":   {"compressed": 1,
                             "optimize": 1,
                             "ascii": 1,
                             "bundle_files": 1}},
    zipfile = None,
    # targets to build
    console = [console_app],
    )
