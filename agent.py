from cli.command import parseCLI
from transform.parser import Parser
from api.server import run

if __name__ == '__main__':
    args = parseCLI()

    if args['run'] is True:
        file_in = args['--input']
        file_out = args['--output']

        myparser = Parser()
        myparser.parsing(file_in)

    elif args['server'] is True:
        port = int(args['--port'])

        run(app="api.server:application", port=port)
