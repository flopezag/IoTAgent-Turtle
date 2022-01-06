import sys
from transform.transformer import TreeToJson
from lark import Lark
from pprint import pprint


def init():
    # Open the grammar file
    with open("./grammar/grammar1.lark") as f:
        grammar = f.read()

    parser = Lark(grammar, start='start', parser='lalr')

    return parser


if __name__ == '__main__':
    myparser = init()
    transform = TreeToJson()

    with open(sys.argv[1]) as f:
        tree = myparser.parse(f.read())
        par = transform.transform(tree)

    pprint(transform.get_context())
    pprint(transform.get_dataset())
    [pprint(x.get()) for x in transform.get_dimensions()]
    [pprint(x.get()) for x in transform.get_concept_schemas()]
