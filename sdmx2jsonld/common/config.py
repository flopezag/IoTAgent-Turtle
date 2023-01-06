from os.path import join, exists, dirname, abspath

# Settings file is inside Basics directory, therefore I have to go back to the parent directory
# to have the Code Home directory
MODULEHOME = dirname(dirname(abspath(__file__)))
GRAMMARFOLDER = join(MODULEHOME, 'grammar')
GRAMMARFILE = join(GRAMMARFOLDER, 'grammar.lark')

if not exists(GRAMMARFILE):
    msg = '\nERROR: There is not Lark grammar file in the expected folder. ' \
          '\n       Unable to parse the RDF Turtle file.' \
          '\n\n       Please correct it if you do not want to see these messages.\n\n\n'

    print(msg)

    exit(1)
