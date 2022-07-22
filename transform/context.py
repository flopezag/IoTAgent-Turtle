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

class Context:
    def __init__(self):
        self.context = {
            "@context": dict()
        }

        # Dictionary to keep those contexts that are update from the core contexts
        self.context_mapping = dict()

        # By default, the context should include the smart data models context
        # TODO: Maybe we can reduce the context management taking into account the details
        self.context['@context']\
            .update({'sdmp': 'https://smart-data-models.github.io/dataModel.STAT-DCAT-AP/context.jsonld'})

        # statDCAT-AP contexts
        self.context['@context']\
            .update({'dcat': 'http://www.w3.org/ns/dcat#'})

        self.context['@context']\
            .update({'dct': 'http://purl.org/dc/terms/'})

        self.context['@context']\
            .update({'stat': 'http://data.europa.eu/(xyz)/statdcat-ap/'})

    def add_context(self, context):
        aux = list(context.items())
        key = aux[0][0]
        value = aux[0][1]

        found = False

        # check is the value of the new_context is in one of the values of the previous context
        for k, v in self.context['@context'].items():
            if v == value:
                found = True
                break

        if not found:
            # we did not find a key -> New context, we need to add
            self.context['@context'].update(context)
        else:
            # We found then we need to change the key in the context or add new one and delete the old one
            self.context['@context'].update(context)
            self.context['@context'].pop(k)
            self.context_mapping.update({k: key})

    def get_context(self):
        return self.context

    def get_context_mapping(self):
        return self.context_mapping

    def print_context(self):
        print(self.context)


if __name__ == '__main__':
    a = Context()

    a.print_context()
    a.add_context({'rdf': '<http://www.w3.org/1999/02/22-rdf-syntax-ns#>'})
    a.print_context()
