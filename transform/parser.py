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

from transform.transformer import TreeToJson
from lark import Lark
from pprint import pprint
from io import TextIOWrapper
from json import dumps
from logging import getLogger
from lark.exceptions import UnexpectedToken, UnexpectedEOF, UnexpectedInput
from common.rdf import turtle_terse


logger = getLogger(__name__)


class Parser:
    def __init__(self):
        # Open the grammar file
        with open("./grammar/grammar.lark") as f:
            grammar = f.read()

        self.parser = Lark(grammar, start='start', parser='lalr')

    def parsing(self, file: TextIOWrapper = None, out: bool = False, content=None):
        transform = TreeToJson()

        if file is not None:
            content = file.read()
            content = turtle_terse(rdf_content=content)

            try:
                tree = self.parser.parse(content)
            except UnexpectedToken as err:
                raise err
            except UnexpectedInput as err:
                raise err
            except UnexpectedEOF as err:
                raise err

            transform.transform(tree)

            if out:
                # Save the generated content into files
                logger.info('Save the generated content into files')
                transform.save()
            elif file is not None:
                print()
                pprint(transform.get_dataset())
                [pprint(x.get()) for x in transform.get_dimensions()]
                [pprint(x.get()) for x in transform.get_attributes()]
                [pprint(x.get()) for x in transform.get_conceptSchemas()]
                [pprint(x.get()) for x in transform.get_conceptLists()]
        elif content is not None:
            # file is an UploadFile aka File
            content = turtle_terse(rdf_content=content)

            tree = self.parser.parse(content)
            transform.transform(tree)

            # Serializing json payload
            result = list()
            result.append(transform.get_dataset())
            [result.append(x.get()) for x in transform.get_dimensions()]
            [result.append(x.get()) for x in transform.get_attributes()]
            [result.append(x.get()) for x in transform.get_conceptSchemas()]
            [result.append(x.get()) for x in transform.get_conceptLists()]

            json_object = dumps(result, indent=4, ensure_ascii=False)

            # with open("final.jsonld", "w") as outfile:
            #     outfile.write(json_object)

            return json_object
