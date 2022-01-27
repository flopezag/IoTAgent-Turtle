from cli.command import parseCLI
from transform.parser import Parser
from api.server import run
from datetime import datetime

if __name__ == '__main__':
    now = datetime.now()

    args = parseCLI()

    if args['run'] is True:
        file_in = args['--input']
        file_out = args['--output']

        myparser = Parser()
        myparser.parsing(file=file_in, out=file_out)
    elif args['server'] is True:
        port = int(args['--port'])

        run(app="api.server:application", port=port, uptime=now)
