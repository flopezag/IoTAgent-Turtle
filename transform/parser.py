from transform.transformer import TreeToJson
from lark import Lark
from pprint import pprint
from io import TextIOWrapper
from json import dumps

class Parser:
    def __init__(self):
        # Open the grammar file
        with open("./grammar/grammar.lark") as f:
            grammar = f.read()

        self.parser = Lark(grammar, start='start', parser='lalr')

    def parsing(self, file:TextIOWrapper=None, out:bool=False, content=None):
        transform = TreeToJson()

        if file is not None:
            content = file.read()
            tree = self.parser.parse(content)
            transform.transform(tree)

            if out:
                # Save the generated content into files
                print('Save the generated content into files')
                transform.save()
            elif file is not None:
                pprint(transform.get_context())
                pprint(transform.get_dataset())
                [pprint(x.get()) for x in transform.get_dimensions()]
                [pprint(x.get()) for x in transform.get_attributes()]
                [pprint(x.get()) for x in transform.get_concept_schemas()]
                [pprint(x.get()) for x in transform.get_code_lists()]
        elif content is not None:
            # file is an UploadFile aka File
            tree = self.parser.parse(content)
            transform.transform(tree)

            # Generate Batch payload with all entities
            result = list()
            result.append(transform.get_dataset())
            [result.append(x.get()) for x in transform.get_dimensions()]
            [result.append(x.get()) for x in transform.get_concept_schemas()]
            [result.append(x.get()) for x in transform.get_code_lists()]

            # Writing to final.json
            # Serializing json
            json_object = dumps(result, indent=4, ensure_ascii=False)

            with open("final.jsonld", "w") as outfile:
                outfile.write(json_object)




if __name__ == '__main__':
    myparser = Parser()
    myparser.parsing("a file")
