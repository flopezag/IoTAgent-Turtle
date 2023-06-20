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

from logging import getLogger
from sdmx2jsonld.common.commonclass import CommonClass
from sdmx2jsonld.common.listmanagement import get_rest_data
from sdmx2jsonld.transform.context import Context

from sdmx2jsonld.sdmxdimensions.frequency import Frequency
from sdmx2jsonld.sdmxdimensions.refarea import RefArea
from sdmx2jsonld.sdmxdimensions.timeperiod import TimePeriod

from sdmx2jsonld.sdmxattributes.observationStatus import ObsStatus
from sdmx2jsonld.sdmxattributes.confirmationStatus import ConfStatus
from sdmx2jsonld.sdmxattributes.timeFormat import TimeFormat
from sdmx2jsonld.sdmxattributes.timePerCollect import TimePerCollect
from sdmx2jsonld.sdmxattributes.decimals import Decimals
from sdmx2jsonld.sdmxattributes.title import Title
from sdmx2jsonld.sdmxattributes.unitmult import UnitMult
from sdmx2jsonld.sdmxattributes.compilingorg import CompilingOrg
from sdmx2jsonld.sdmxattributes.dataComp import DataComp
from sdmx2jsonld.sdmxattributes.currency import Currency
from sdmx2jsonld.sdmxattributes.dissorg import DissOrg

from sdmx2jsonld.sdmxconcepts.freqconcept import FreqConcept
from sdmx2jsonld.sdmxconcepts.cogconceptschema import CogConceptSchema
from sdmx2jsonld.sdmxconcepts.timeperiodconcept import TimePeriodConcept
from sdmx2jsonld.sdmxconcepts.refareaconcept import RefAreaConcept
from sdmx2jsonld.sdmxconcepts.obsstatusconcept import ObsStatusConcept
from sdmx2jsonld.sdmxconcepts.confstatusconcept import ConfStatusConcept
from sdmx2jsonld.sdmxconcepts.timeformatconcept import TimeFormatConcept
from sdmx2jsonld.sdmxconcepts.timePerCollectConcept import TimePerCollectConcept
from sdmx2jsonld.sdmxconcepts.decimals import DecimalsConcept
from sdmx2jsonld.sdmxconcepts.titleConcept import TitleConcept
from sdmx2jsonld.sdmxconcepts.unitmultconcept import UnitMultConcept
from sdmx2jsonld.sdmxconcepts.compilingorgconcept import CompilingOrgConcept
from sdmx2jsonld.sdmxconcepts.datacompconcept import DataCompConcept
from sdmx2jsonld.sdmxconcepts.currencyconcept import CurrencyConcept
from sdmx2jsonld.sdmxconcepts.dissorgconcept import DissOrgConcept

logger = getLogger()


class Dataset(CommonClass):
    def __init__(self):
        super().__init__(entity='Dataset')

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

        self.components = {
            'qb:attribute': {
                'entity': 'AttributeProperty',
                'key': 'stat:attribute',
                'value': {
                    "stat:attribute": {
                        "type": "Relationship",
                        "object": list()
                    }
                }
            },
            'qb:dimension': {
                'entity': 'DimensionProperty',
                'key': 'stat:dimension',
                'value': {
                    "stat:dimension": {
                        "type": "Relationship",
                        "object": list()
                    }
                }
            },
            'qb:measure': {
                'entity': 'Measure',
                'key': 'stat:statUnitMeasure',
                'value': {
                    "stat:statUnitMeasure": {
                        "type": "Relationship",
                        "object": list()
                    }
                }
            }
        }

        self.keys = {k: k for k in self.data.keys()} | \
                    {self.components['qb:attribute']['key']: self.components['qb:attribute']['key']} | \
                    {self.components['qb:dimension']['key']: self.components['qb:dimension']['key']} | \
                    {self.components['qb:measure']['key']: self.components['qb:measure']['key']}

        self.sdmx_dimensions = {
            "freq": Frequency(),
            "refArea": RefArea(),
            "timePeriod": TimePeriod()
        }

        self.sdmx_attributes = {
            "obsStatus": ObsStatus(),
            "confStatus": ConfStatus(),
            "timeFormat": TimeFormat(),
            "timePerCollect": TimePerCollect(),
            "decimals": Decimals(),
            "title": Title(),
            "unitMult": UnitMult(),
            "compilingOrg": CompilingOrg(),
            "dataComp": DataComp(),
            "dissOrg": DissOrg(),
            "currency": Currency()
        }

        self.sdmx_components = {
            "DimensionProperty": self.sdmx_dimensions,
            "AttributeProperty": self.sdmx_attributes
        }

        self.sdmx_concepts = {
            "freq": FreqConcept(),
            "refArea": RefAreaConcept(),
            "timePeriod": TimePeriodConcept(),
            "obsStatus": ObsStatusConcept(),
            "confStatus": ConfStatusConcept(),
            "timeFormat": TimeFormatConcept(),
            "timePerCollect": TimePerCollectConcept(),
            "decimals": DecimalsConcept(),
            "title": TitleConcept(),
            "unitMult": UnitMultConcept(),
            "compilingOrg": CompilingOrgConcept(),
            "dataComp": DataCompConcept(),
            "dissOrg": DissOrgConcept(),
            "currency": CurrencyConcept()
        }

        self.sdmx_concept_schemas = CogConceptSchema()

    def add_components(self, context, component):
        # We need to know which kind of component we have, it should be the verb:
        # qb:attribute, qb:dimension, or qb:measure
        list_components = ['qb:attribute', 'qb:dimension', 'qb:measure']

        # TODO: These dimensions are not defined in the turtle file but defined in a prefix therefore at the moment
        # we create manually their corresponding DimensionProperty entity. Should we generated from checking the prefix
        list_special_components = ['freq', 'refArea', 'timePeriod',
                                   'obsStatus', 'confStatus', 'timeFormat',
                                   'timePerCollect', 'decimals', 'title',
                                   'unitMult', 'compilingOrg', 'dataComp',
                                   'currency', 'dissOrg']

        type_component = [x for x in list_components if x in component][0]
        position = component.index(type_component) + 1

        try:
            entity = self.components[type_component]['entity']
            name, new_id = self.generate_id(entity=entity, value=component[position][0], update_id=False)
            key = self.components[type_component]['key']

            # It is possible that the original file contains already the description
            if new_id in self.components[type_component]['value'][key]['object']:
                logger.warning(
                    f"The component {new_id} is duplicated and already defined in the {self.data['id']}")
            elif name in list_special_components:
                # We need to create manually the description of these dimensions, concepts, and conceptschemas
                logger.warning(
                    f"The component {name} is defined probably outside of the file, "
                    f"creating manually the {entity} entity")
                self.components[type_component]['value'][key]['object'].append(new_id)
                self.data = self.data | self.components[type_component]['value']

                new_component = self.sdmx_components[entity]
                new_dimension = new_component[name]
                new_concept = self.sdmx_concepts[name]
                new_concept_schema = self.sdmx_concept_schemas

                return new_dimension, new_concept, new_concept_schema
            else:
                self.components[type_component]['value'][key]['object'].append(new_id)
                self.data = self.data | self.components[type_component]['value']
        except ValueError:
            logger.error(f"Error, it was identified a qb:ComponentSpecification with a wrong type: {type_component}")

        # Simplify Context and order keys. It is possible that we call add_component before the dataset has been created
        # therefore we need to add the corresponding context to the dataset
        if len(self.data['@context']) == 0:
            self.data['@context'] = context['@context']

        a = Context()
        a.set_data(data=self.data)
        a.new_analysis()
        a.order_context()
        self.data = a.get_data()

        return None, None, None

    def get(self):
        return self.data

    def add_data(self, title, dataset_id, data):
        # We need to complete the data corresponding to the Dataset: rdfs:label
        self.__complete_label__(title=title, data=data)

        # Add the title
        key = self.keys['dct:title']
        self.data[key] = title

        # Add the id
        self.data['id'] = "urn:ngsi-ld:Dataset:" + dataset_id

        # Get the rest of the data
        data = get_rest_data(data=data,
                             not_allowed_keys=[
                                 'sliceKey',
                                 'component',
                                 'disseminationStatus',
                                 'validationState',
                                 'notation',
                                 'label'
                             ],
                             further_process_keys=[
                                 'component',
                                 'label'
                             ])

        # add the new data to the dataset structure
        self.patch_data(data, False)

    def patch_data(self, data, language_map):
        if language_map:
            self.__complete_label__(title="Not specified", data=data)
        else:
            # TODO: Add only those properties that are expected, if they are not know or unexpected discard and provide
            #  a logging about the property is discarded due to it is not considered in the statSCAT-AP spec.
            [self.data.update(self.__generate_property__(key=k, value=v)) for k, v in data.items()]

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
