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

        # By default, the context should include the smart data models context
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
        self.context['@context'].update(context)

    def get_context(self):
        return self.context

    def print_context(self):
        print(self.context)


if __name__ == '__main__':
    a = Context()

    a.print_context()
    a.add_context({'rdf': '<http://www.w3.org/1999/02/22-rdf-syntax-ns#>'})
    a.print_context()
