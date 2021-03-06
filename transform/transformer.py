#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##
# Copyright 2022 FIWARE Foundation, e.V.
#
# This file is part of IoTAgent-SDMX (RDF Turtle)
#
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
##

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

    def get_conceptSchemas(self):
        return self.entity_type.get_conceptSchemas()

    def get_conceptLists(self):
        return self.entity_type.get_conceptList()

    def save(self):
        self.entity_type.save('dataset')

        dimensions = self.entity_type.get_dimensions()
        [dimension.save() for dimension in dimensions]

        attributes = self.entity_type.get_attributes()
        [attribute.save() for attribute in attributes]

        concept_schemas = self.entity_type.get_conceptSchemas()
        [x.save() for x in concept_schemas]

        # TODO: The current version does not upload content related to Concepts
        #       and Range of values of these Concepts
        # conceptLists = self.entity_type.get_conceptList()
        # [x.save() for x in conceptLists]

