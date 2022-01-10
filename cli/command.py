"""Naval Fate.

Usage:
  agent.py run (--input FILEIN) [--output FILEOUT]
  agent.py server [--port PORT]
  agent.py (-h | --help)
  agent.py --version

Options:
  -i FILEIN --input=FILEIN  when parsing directories, only check filenames matching
                            these comma separated patterns.
                            [default: file.ttl]
  -o FILEOUT --output=FILEOUT  when parsing directories, only check filenames matching
                               these comma separated patterns.
  -p PORT --port=PORT    Launch the server in the corresponding Port
                         [default: 5000]

  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
from os.path import basename
from sys import argv

__version__ = "0.1.0"
__author__ = "fla"


def parseCLI() -> dict:
    arguments = docopt(__doc__, version='IoTAgent RDF Turtle parser to NGSI-LD')
    version = f"{__name__} {__version__}"
    args = docopt(__doc__.format(proc=basename(argv[0])), version=version)

    return args


if __name__ == '__main__':
    print(parseCLI())
