from lark import Transformer, Tree, Token
from transform.context import Context
from transform.entitytype import EntityType


class TreeToJson(Transformer):
    def __init__(self):
        self.context = Context()
        self.entity_type = EntityType()

    def prefixid(self, s):
        context = dict()
        context[str(s[0].children[0])] = s[1]
        self.context.add_context(context)

    def triples(self, triple):
        self.entity_type.transform(string=triple)
        return triple

    def predicate(self, pre):
        result = ''
        if isinstance(pre[0], str):
            result = pre[0]
        else:
            result = str(pre[0].children[0].children[0])

        return result

    def subject(self, sub):
        # sub[0].children can be a Token 'URIREF' -> e.g. <http://data.europa.eu/nuts/scheme/2016>
        # or Tree -> e.g. Tree(Token('RULE', 'iri'), [Tree(Token('RULE', 'prefixedname'), [Token('PNAME_LN', 'isc:dsd1')])])
        result = ''
        if isinstance(sub[0], str):
            result = sub[0]
        elif isinstance(sub[0].children[0], str):
            result = sub[0].children[0]
        else:
            result = str(sub[0].children[0].children[0])

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

    def blanknodepropertylist(self, property_list):
        self.entity_type.transform(string=property_list)
        return property_list

    def get_context(self):
        return self.context.get_context()

    def get_dataset(self):
        return self.entity_type.get_dataset()

    def get_dimensions(self):
        return self.entity_type.get_dimensions()

    def get_concept_schemas(self):
        return self.entity_type.get_concept_schemas()

    def get_code_lists(self):
        return self.entity_type.get_code_lists()
