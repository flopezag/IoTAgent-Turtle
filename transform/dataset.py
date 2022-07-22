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

        self.keys = {k: k for k in self.data.keys()} | \
                    {k: k for k in self.dimensions.keys()} | \
                    {k: k for k in self.attributes.keys()} | \
                    {k: k for k in self.unitMeasures.keys()}

    def add_components(self, component):
        # We need to know which kind of component we have, it should be the verb:
        # qb:attribute, qb:dimension, or qb:measure
        type_component = [x for x in ['qb:attribute', 'qb:dimension', 'qb:measure'] if x in component][0]
        position = component.index(type_component) + 1

        if type_component == 'qb:attribute':
            new_id = self.__generate_id__(entity="AttributeProperty", value=component[position][0])
            key = self.keys['stat:attribute']
            self.attributes[key]['value'].append(new_id)
        elif type_component == 'qb:dimension':
            new_id = self.__generate_id__(entity="DimensionProperty", value=component[position][0])
            key = self.keys['stat:dimension']
            self.dimensions[key]['value'].append(new_id)
        elif type_component == 'qb:measure':
            new_id = self.__generate_id__(entity="Measure", value=component[position][0])
            key = self.keys['stat:statUnitMeasure']
            self.unitMeasures[key]['value'].append(new_id)
        else:
            print(f"Error, it was identified a qb:ComponentSpecification with a wrong type: {type_component}")

    @staticmethod
    def __generate_id__(entity, value):
        parse = RegParser()
        aux = parse.obtain_id(value)
        aux = "urn:ngsi-ld:" + entity + ":" + aux
        return aux

    def get(self):
        key = self.keys['stat:dimension']
        if len(self.dimensions[key]['value']) != 0:
            self.data = self.data | self.dimensions

        key = self.keys['stat:attribute']
        if len(self.attributes[key]['value']) != 0:
            self.data = self.data | self.attributes

        key = self.keys['stat:statUnitMeasure']
        if len(self.unitMeasures[key]['value']) != 0:
            self.data = self.data | self.unitMeasures

        return self.data

    def add_data(self, title, dataset_id, data):
        # We need to complete the data corresponding to the Dataset: rdfs:label
        self.__complete_label__(title=title, data=data)

        # Add the title
        key = self.keys['dct:title']
        self.data[key] = title

        # Add the id
        self.data['id'] = "urn:ngsi-ld:Dataset:" + dataset_id

        data = self.get_rest_data(data=data)

        # add the new data to the dataset structure
        self.patch_data(data, False)

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

        key = self.keys['id']
        aux = data[key].split(":")
        length_aux = len(aux)
        filename = '_'.join(aux[length_aux - 2:]) + '.jsonld'

        # Serializing json
        json_object = dumps(data, indent=4, ensure_ascii=False)

        # Writing to sample.json
        with open(filename, "w") as outfile:
            outfile.write(json_object)

    def patch_data(self, data, language_map):
        if language_map:
            self.__complete_label__(title="Not specified", data=data)
        else:
            # TODO: Add only those properties that are expected, if they are not know or unexpected discard and provide
            #  a logging about the property is discarded due to it is not considered in the statSCAT-AP spec.
            [self.data.update({k: v}) for k, v in data.items()]

    def __complete_label__(self, title, data):
        try:
            key = self.get_key(requested_key='rdfs:label')
            position = data.index(key) + 1
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
                key = self.keys['dct:description']
                self.data[key]['value'][languages[i]] = descriptions[i]

            # Complete the information of the language with the previous information
            key = self.keys['dct:language']
            self.data[key]['value'] = languages
        except ValueError:
            logger.info(f'DataStructureDefinition without rdfs:label detail: {title}')

    def get_key(self, requested_key):
        try:
            key = self.keys[requested_key]
            return key
        except KeyError:
            # The key did not exist therefore we add to the list with this value
            self.keys[requested_key] = requested_key
            return requested_key

    @staticmethod
    def get_rest_data(data):
        def filter_key_with_prefix(prefix_key):
            aux = prefix_key.split(":")

            # We dismiss the following keys to be analysed due to they are not manage in the current version of
            # statDCAT-AP (sliceKey, disseminationStatus, validationState, notation), they are manage in a separate
            # process (label) or manage afterward analysing the turtle file (component)
            # TODO: we should keep component in order to check that afterwards we get the definition of that component
            not_allowed_keys = ['sliceKey',
                                'component',
                                'disseminationStatus',
                                'validationState',
                                'notation',
                                'label']

            if len(aux) == 2:
                if aux[1] not in not_allowed_keys:
                    # this is a key with prefix that we want to keep
                    return True
                else:
                    if aux[1] not in ['component', 'label']:
                        # These are the identified not allowed keys, we need to inform about them
                        logger.warn(f'The property {aux[1]} is not supported in statDCAT-AP')
                    else:
                        # These are the identified keys managed in a different way
                        logger.info(f'The property {aux[1]} is manage afterwards in Dataset Class or in Property Class')

                    return False
            else:
                return False

        def flatten_value(y):
            if isinstance(y, list):
                return flatten_value(y[0])
            else:
                return y.replace('"', '')

        aux = {data[i]:  flatten_value(data[i + 1]) for i in range(0, len(data), 2)}

        # We need to get the list of keys from the dict
        new_keys = list(filter(lambda x: filter_key_with_prefix(x), list(aux.keys())))
        new_data = {k: aux[k] for k in new_keys}

        return new_data
