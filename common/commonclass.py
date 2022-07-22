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
from json import dumps


class CommonClass:
    def __init__(self):
        self.data = dict()
        self.keys = dict()

    def add_context(self, context, context_mapping):
        # TODO: We should assign only the needed context and not all the contexts
        # Set the context as it is received and mixed with the core context
        self.data['@context'] = context['@context']

        # Fix the prefix of the core properties of the Dataset entity
        new_data = dict()

        for k, v in self.data.items():
            # Return if the string matched the ReGex
            out = k.split(':')

            if len(out) == 2 and out[0] in context_mapping.keys():
                new_prefix = context_mapping[out[0]]
                new_key = new_prefix + ':' + out[1]

                new_data[new_key] = self.data[k]
                self.keys[k] = new_key
            else:
                new_data[k] = v

        self.data = new_data

    def save(self):
        data = self.get()

        aux = data['id'].split(":")
        length_aux = len(aux)
        filename = '_'.join(aux[length_aux - 2:]) + '.jsonld'

        # Serializing json
        json_object = dumps(data, indent=4, ensure_ascii=False)

        # Writing to sample.json
        with open(filename, "w") as outfile:
            outfile.write(json_object)
