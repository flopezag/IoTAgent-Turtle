from sdmx2jsonld.transform.parser import Parser
from sdmx2jsonld.exceptions import UnexpectedEOF, UnexpectedInput, UnexpectedToken

if __name__ == "__main__":
    # file_in = open("../examples/structures-accounts.ttl")
    file_in = open("kex/e1.ttl")
    generate_files = True

    # Start parsing the file
    my_parser = Parser()

    try:
        my_parser.parsing(content=file_in, out=generate_files)
    except UnexpectedToken as e:
        print(e)
    except UnexpectedInput as e:
        print(e)
    except UnexpectedEOF as e:
        print(e)
