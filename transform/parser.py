from transform.transformer import TreeToJson
from lark import Lark
from pprint import pprint
from io import TextIOWrapper

class Parser:
    def __init__(self):
        # Open the grammar file
        with open("./grammar/grammar.lark") as f:
            grammar = f.read()

        self.parser = Lark(grammar, start='start', parser='lalr')

    def parsing(self, file:TextIOWrapper=None, out:bool=False, content=None):
        transform = TreeToJson()

        if file is not None:
            tree = self.parser.parse(file.read())
            transform.transform(tree)
        elif content is not None:
            # file is an UploadFile aka File
            tree = self.parser.parse(content)
            transform.transform(tree)

        if out:
            # Save the generated content into files
            print('Save the generated content into files')
        else:
            pprint(transform.get_context())
            pprint(transform.get_dataset())
            [pprint(x.get()) for x in transform.get_dimensions()]
            [pprint(x) for x in transform.get_concept_schemas()]
            [pprint(x) for x in transform.get_code_lists()]


if __name__ == '__main__':
    myparser = Parser()
    myparser.parsing("a file")
