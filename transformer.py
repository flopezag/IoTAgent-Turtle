from lark import Transformer


# class TreeToJson(Transformer):
#     @inline_args
#     def string(self, s):
#         return s[1:-1].replace('\\"', '"')
#
#     array = list
#     pair = tuple
#     object = dict
#     number = inline_args(float)
#
#     null = lambda self, _: None
#     true = lambda self, _: True
#     false = lambda self, _: False


class TreeToJson(Transformer):
    def prefixid(self, s):
        print(s[1], s[3])

    def prefixname(self, name):
        return ''.join([str(x) for x in name])

    def uriref(self, uri):
        return ''.join([str(x) for x in uri])
