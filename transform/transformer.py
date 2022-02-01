from lark import Transformer, Tree, Token
from transform.context import Context
from transform.entitytype import EntityType
import re


class TreeToJson(Transformer):
    def __init__(self):
        super().__init__()
        self.context = Context()
        self.entity_type = EntityType()

        # Regex to check valid URL
        regex = "<http[s]?:\/\/(.*)>"

        # Compile the Regex
        self.re = re.compile(regex)

    def prefixid(self, s):
        context = dict()
        context[str(s[0].children[0])] = s[1]
        self.context.add_context(context)

    def triples(self, triple):
        self.entity_type.transform(string=triple, context=self.get_context())
        return triple

    def predicate(self, pre):
        result = ''
        if isinstance(pre[0], str):
            result = pre[0]
        else:
            result = str(pre[0].children[0].children[0])

        return result

    def subject(self, sub):
        # sub[0] can be an URIREF or a prefixedname
        result = str()

        # Return if the string matched the ReGex
        out = self.re.match(sub[0])

        if out == None:
            # We have a prefixedname subject
            result = sub[0]
        else:
            # We have a URIREF
            out = out.group(1)
            out = out.split("/")

            # we get the last 2 values to compose the proper subject
            out = out[(len(out) - 2):]
            result = '_'.join(out)

        return result

    def predicateobjectlist(self, pol):
        return pol

    def objectlist(self, ol):
        return ol

    def prefixedname(self, pre):
        return str(pre[0])

    def string(self, a):
        return str(a[0])

    def rdfliteral(self, a):
        return a

    def langtag(self, tag):
        return str(tag[0])

    def iri(self, iri):
        return str(iri[0])

    def verb(self, verb):
        return str(verb[0])

    def object(self, object):
        return object[0]

    def literal(self, literal):
        return literal[0]

    def uriref(self, uriref):
        return str(uriref[0])

    def blanknodepropertylist(self, property_list):
        self.entity_type.transform(string=property_list, context=self.get_context())
        return property_list

    def get_context(self):
        return self.context.get_context()

    def get_dataset(self):
        return self.entity_type.get_dataset()

    def get_dimensions(self):
        return self.entity_type.get_dimensions()

    def get_attributes(self):
        return self.entity_type.get_attributes()

    def get_concept_schemas(self):
        return self.entity_type.get_concept_schemas()

    def get_code_lists(self):
        return self.entity_type.get_code_lists()

    def save(self):
        self.entity_type.save('dataset')

        dimensions = self.entity_type.get_dimensions()
        [dimension.save() for dimension in dimensions]

        concept_schemas = self.entity_type.get_concept_schemas()
        [x.save() for x in concept_schemas]

        code_lists = self.entity_type.get_code_lists()
        [x.save() for x in code_lists]

