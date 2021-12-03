import sys
from transformer import TreeToJson
from lark import Lark


def init():
    # Open the grammar file
    with open("./grammar/grammar.lark") as f:
        grammar = f.read()

    parser = Lark(grammar, start='start', parser='earley')

    return parser


if __name__ == '__main__':
    myparser = init()
    transform = TreeToJson()

    with open(sys.argv[1]) as f:
        tree = myparser.parse(f.read())
        par = transform.transform(tree)
    #with open(sys.argv[1]) as f:
    #    print(json_parser.parse(f.read()))