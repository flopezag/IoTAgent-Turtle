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
from logging import getLogger

logger = getLogger()


class Property:
    def __init__(self):
        self.data = {
            "id": str(),
            "type": "",


            #################################################
            # TODO: New ETSI CIM NGSI-LD specification 1.4.2
            # Pending to implement in the Context Broker
            #################################################
            # "rdfs:label": {
            #     "type": "LanguageProperty",
            #     "LanguageMap": dict()
            # },
            #################################################
            "rdfs:label": {
                "type": "Property",
                "value": dict()
            },


            "qb:codeList": {
                "type": "Relationship",
                "object": str()
            },
            "qb:concept": {
                "type": "Property",
                "value": str()
            },
            "@context": dict()
        }

    def add_data(self, id, data):
        # TODO: We have to control that data include the indexes that we want to search
        # We need to complete the data corresponding to the Dimension: rdfs:label
        position = data.index('rdfs:label') + 1
        description = data[position]

        descriptions = [x[0].replace("\"", "") for x in description]

        languages = list()
        try:
            languages = [x[1].replace("@", "").lower() for x in description]
        except IndexError:
            logger.warning(f'The Property {id} has a '
                           f'rdfs:label without language tag: {description}')

            aux = len(description)
            if aux != 1:
                logger.error(f"Property: there is more than 1 description ({aux}), values: {description}")
            else:
                # There is no language tag, we use by default 'en'
                languages = ['en']
                logger.warning('Property: selecting default language "en"')

        ###############################################################################
        # TODO: New ETSI CIM NGSI-LD specification 1.4.2
        # Pending to implement in the Context Broker
        ###############################################################################
        # for i in range(0, len(languages)):
        #     self.data['rdfs:label']['LanguageMap'][languages[i]] = descriptions[i]
        ###############################################################################
        for i in range(0, len(languages)):
            self.data['rdfs:label']['value'][languages[i]] = descriptions[i]

        # qb:codeList
        position = data.index('qb:codeList') + 1
        code_list = data[position][0]
        code_list = code_list.split(":")
        code_list = "urn:ngsi-ld:ConceptSchema:" + code_list[len(code_list)-1]
        self.data['qb:codeList']['object'] = code_list

        # qb:concept
        position = data.index('qb:concept') + 1
        concept = data[position][0]
        self.data['qb:concept']['value'] = concept


    def add_context(self, context):
        # TODO: We should assign only the needed context and not all the contexts
        self.data['@context'] = context['@context']

    def get(self):
        return self.data

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
