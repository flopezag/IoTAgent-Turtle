"""IoTAgent RDF Turtle parser to NGSI-LD

Usage:
  agent.py run (--input FILE) [--output]
  agent.py server [--port PORT]
  agent.py (-h | --help)
  agent.py --version

Arguments:
  FILE   input file
  PORT   http port used by the service

Options:
  -i, --input FILEIN  specify the RDF turtle file to parser
  -o, --output        generate the corresponding files of the parser RDF turtle file
  -p, --port PORT     launch the server in the corresponding Port
                      [default: 5000]

  -h, --help          show this help message and exit
  -v, --version       show version and exit

"""
from docopt import docopt
from os.path import basename
from sys import argv
from schema import Schema, And, Or, Use, SchemaError

__version__ = "0.1.0"
__author__ = "fla"


def parseCLI() -> dict:
    if len(argv) == 1:
        argv.append('-h')

    version = f'IoTAgent-Turtle version {__version__}'

    args = docopt(__doc__.format(proc=basename(argv[0])), version=version)

    schema = Schema(
        {
            '--help': bool,
            '--input': Or(None, Use(open, error='--input FILE, FILE should be readable')),
            '--output': bool,
            '--port': Or(None, And(Use(int), lambda n: 1 < n < 65535),
                      error='--port N, N should be integer 1 < N < 65535'),
            '--version': bool,
            'run': bool,
            'server': bool
        }
    )

    try:
        args = schema.validate(args)
    except SchemaError as e:
        exit(e)

    return args


if __name__ == '__main__':
    print(parseCLI())
