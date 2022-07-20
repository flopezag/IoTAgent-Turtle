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
from common.regparser import RegParser

logger = getLogger()


class Dataset:
    def __init__(self):
        self.allowed_keys = [
                'id',
                'type',
                'dct:title',
                'dct:identifier',
                'dct:language',
                'dct:description',
                'stat:dimension',
                'stat:attribute',
                'stat:statUnitMeasure',
                'dc:contributor',
                'dc:creator',
                'dct:created',
                'dct:modified',
                'qb:component',
                'qb:sliceKey',
                'skos:notation'
        ]

        self.data = {
            "id": str(),
            "type": "Dataset",
            "dct:title": str(),
            "dct:identifier": str(),
            "dct:language": {
                "type": "Property",
                "value": list()
            },


            #################################################
            # TODO: New ETSI CIM NGSI-LD specification 1.4.2
            # Pending to implement in the Context Broker
            #################################################
            # "rdfs:label": {
            #     "type": "LanguageProperty",
            #     "LanguageMap": dict()
            # },
            #################################################
            "dct:description": {
                "type": "Property",
                "value": dict()
            },


            "@context": dict()
        }

        self.dimensions = {
            "stat:dimension": {
                "type": "Property",
                "value": list()
            }
        }

        self.attributes = {
            "stat:attribute": {
                "type": "Property",
                "value": list()
            }
        }

        self.unitMeasures = {
            "stat:statUnitMeasure": {
                "type": "Property",
                "value": list()
            }
        }

    def add_components(self, component):
        # We need to know which kind of component we have, it should be the verb:
        # qb:attribute, qb:dimension, or qb:measure
        type_component = [x for x in ['qb:attribute', 'qb:dimension', 'qb:measure'] if x in component][0]
        position = component.index(type_component) + 1

        if type_component == 'qb:attribute':
            id = self.__generate_id__(entity="AttributeProperty", value=component[position][0])
            self.attributes['stat:attribute']['value'].append(id)
        elif type_component == 'qb:dimension':
            id = self.__generate_id__(entity="DimensionProperty", value=component[position][0])
            self.dimensions['stat:dimension']['value'].append(id)
        elif type_component == 'qb:measure':
            id = self.__generate_id__(entity="Measure", value=component[position][0])
            self.unitMeasures['stat:statUnitMeasure']['value'].append(id)
        else:
            print(f"Error, it was identified a qb:ComponentSpecification with a wrong type: {type_component}")

    def __generate_id__(self, entity, value):
        parse = RegParser()
        aux = parse.obtain_id(value)
        # aux = value.split(":")
        # aux = "urn:ngsi-ld:" + entity + ":" + aux[len(aux)-1]
        aux = "urn:ngsi-ld:" + entity + ":" + aux
        return aux

    def get(self):
        self.data = self.data | self.dimensions | self.attributes | self.unitMeasures
        return self.data

    def add_data(self, title, id, data):
        # TODO: We have to control that data include the indexes that we want to search
        # We need to complete the data corresponding to the Dataset: rdfs:label
        self.__complete_label__(title=title, data=data)

        # Add the title
        self.data['dct:title'] = title

        # Add the id
        self.data['id'] = "urn:ngsi-ld:Dataset:" + id

        # Add the id
        # self.data['dct:identifier'] = identifier

    def add_context(self, context):
        # TODO: We should assign only the needed context and not all the contexts
        self.data['@context'] = context['@context']

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

    def patch_data(self, data, languageMap):
        if languageMap:
            self.__complete_label__(title="Not spscified", data=data)
        else:
            # TODO: Add only those properties that are expected, if they are not know or unexpected discard and provide
            #  a logging about the property is discarded due to it is not considered in the statSCAT-AP spec.
            [self.data.update({k: v}) for k, v in data.items()]

        print(self.data)
        
    def __complete_label__(self, title, data):
        try:
            position = data.index('rdfs:label') + 1
            description = data[position]

            descriptions = [x[0].replace("\"", "") for x in description]

            languages = list()
            try:
                languages = [x[1].replace("@", "").lower() for x in description]
            except IndexError:
                logger.warning(f'The Dataset {title} has a '
                               f'rdfs:label without language tag: {description}')

                aux = len(description)
                if aux != 1:
                    logger.error(f"Dataset: there is more than 1 description ({aux}), values: {description}")
                else:
                    # There is no language tag, we use by default 'en'
                    languages = ['en']
                    logger.warning('Dataset: selecting default language "en"')

            ###############################################################################
            # TODO: New ETSI CIM NGSI-LD specification 1.4.2
            # Pending to implement in the Context Broker
            ###############################################################################
            # for i in range(0, len(languages)):
            #     self.data['rdfs:label']['LanguageMap'][languages[i]] = descriptions[i]
            ###############################################################################
            for i in range(0, len(languages)):
                self.data['dct:description']['value'][languages[i]] = descriptions[i]

            # Complete the information of the language with the previous information
            self.data['dct:language']['value'] = languages
        except ValueError:
            logger.info(f'DataStructureDefinition without rdfs:label detail: {title}')
