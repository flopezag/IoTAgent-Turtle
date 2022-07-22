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

from transform.dataset import Dataset
from transform.dimension import Dimension
from transform.conceptschema import ConceptSchema
from transform.concept import Concept
from transform.datarange import DataRange
from transform.attribute import Attribute
from logging import getLogger
from datetime import datetime
from common.regparser import RegParser

logger = getLogger()


class EntityType:
    def __init__(self):
        self.entities = {
            'qb:DataStructureDefinition': 'Dataset',
            'qb:ComponentSpecification': 'Component',
            'qb:AttributeProperty': 'Attribute',
            'qb:DimensionProperty': 'Dimension',
            'qb:CodedProperty': 'Dimension',
            'rdfs:Class': 'Class',
            'owl:Class': 'Class',
            'skos:ConceptScheme': 'ConceptScheme',
            'skos:Concept': 'Range'
        }

        self.dataset = Dataset()
        self.dimensions = list()
        self.attributes = list()
        self.conceptSchemas = list()
        self.conceptLists = list()
        self.conceptListsIds = dict()
        self.context = dict()
        self.context_mapping = dict()

    def __find_entity_type__(self, string):
        """
        Find the index position of the 'a' SDMX key and return the following data with the corresponding EntityType
        """
        is_new = bool()

        # Index maybe 0 in case of ComponentSpecification or 1 in case of DataStructureDefinition
        index = len(string) - 1
        string1 = string[index]

        # We can get a 'verb' 'objectlist' or an 'objectlist', where verb is 'a'
        # in case that there is no verb, we are talking about a triples whose id was previously
        # created.
        try:
            position = string1.index('a') + 1
            # data = string[position][0]
            # TODO: if the type is an array we get the last value of the list as the entity type, it should be better
            #  the analyse all the element of the list to find which one should be taken,
            #  e.g., ['DimensionProperty'. 'CodedProperty'] takes 'CodedProperty'
            data = string1[position][len(string1[position]) - 1]

            # We have two options, a well-know object list to be found in the self.entities or
            # the conceptList defined in the turtle file
            try:
                data = self.entities[data]
            except KeyError:
                # We found a CodeList or any other thing, check the list of codeList found in the turtle file
                if data not in self.conceptListsIds:
                    print(f"Received a unexpected entity type: {data}")
                else:
                    data = 'Range'

            is_new = True
        except ValueError:
            logger.info(f'Not a definition triples {string}, need to find the proper structure')
            is_new = False
            data = self.__get_subject__(title=string[0])
            string1 = string[1:]

        return data, string1, is_new

    def transform(self, string):
        if len(self.context) == 0:
            raise AssertionError("Context should be passed before to the EntityType Class, call EntityType.set_context() "
                                 "before, {'__file__': this_file}))")

        data_type, new_string, is_new = self.__find_entity_type__(string=string)

        if is_new:
            self.create_data(type=data_type, data=new_string, title=string[0])
        else:
            logger.info(f'Checking previous subjects to find if it was created previously')
            self.patch_data(datatype=data_type, data=new_string)

    def patch_data(self, datatype, data):
        def flatten_value(y):
            if isinstance(y, list):
                return flatten_value(y[0])
            elif isinstance(y, datetime):
                return y
            else:
                return y.replace('"', '')

        flatten_data = [item for sublist in data for item in sublist]

        if flatten_data[0] != 'rdfs:label':
            flatten_data = {flatten_data[i]: flatten_value(flatten_data[i + 1]) for i in range(0, len(flatten_data), 2)}
            languageMap = False
        else:
            languageMap = True

        if datatype == 'Dataset':
            self.dataset.patch_data(data=flatten_data, languageMap=languageMap)

    def create_data(self, type, data, title):
        parser = RegParser()

        if type == 'Component':
            self.dataset.add_components(component=data)
        elif type == 'Dataset':
            identifier = parser.obtain_id(title)
            self.dataset.add_context(context=self.context, context_mapping=self.context_mapping)
            self.dataset.add_data(title=title, dataset_id=identifier, data=data)
        elif type == 'Dimension':
            dimension = Dimension()
            dimension.add_context(context=self.context)
            dimension_id = parser.obtain_id(title)
            dimension.add_data(id=dimension_id, data=data)
            self.dimensions.append(dimension)
        elif type == 'Attribute':
            attribute = Attribute()
            attribute.add_context(context=self.context)
            attribute_id = title.split(':')[1]
            attribute.add_data(id=attribute_id, data=data)
            self.attributes.append(attribute)
        elif type == 'ConceptScheme':
            conceptSchema = ConceptSchema()
            conceptSchema.add_context(context=self.context)

            if ':' in title:
                aux = title.split(':')[1]
                aux = aux.split('/')
                conceptSchemaId = '_'.join(aux[len(aux)-2:])
            else:
                conceptSchemaId = title

            conceptSchema.add_data(concept_schema_id=conceptSchemaId, data=data)
            self.conceptSchemas.append(conceptSchema)
        elif type == 'Class':
            # We need the Concept because each of the Range description is of the type Concept
            conceptList = Concept()
            conceptList.add_context(context=self.context)
            conceptlistId = title.split(':')[1]
            conceptList.add_data(conceptId=conceptlistId, data=data)
            self.conceptLists.append(conceptList)
            self.conceptListsIds[title] = conceptList.get_id()
        elif type == 'Range':
            data_range = DataRange()
            data_range_id = title.split(':')[1].split('/')
            data_range_id = data_range_id[len(data_range_id)-1]
            data_range.add_data(range_id=data_range_id, data=data)  # ERROR should be all the data not only data, previously was string

            for i in range(0, len(self.conceptSchemas)):
                concept_schema = self.conceptSchemas[i].data
                has_top_concept_values = concept_schema['skos:hasTopConcept']['value']

                out = [data_range.notation if x == data_range.id else x for x in has_top_concept_values]

                self.conceptSchemas[i].data['skos:hasTopConcept']['value'] = out

    def __get_subject__(self, title):
        if self.dataset.get()['dct:title'] == title:
            return 'Dataset'
        else:
            AssertionError(f"Still not defined: {title}")

    def get_dataset(self):
        return self.dataset.get()

    def get_dimensions(self):
        return self.dimensions

    def get_attributes(self):
        return self.attributes

    def get_conceptSchemas(self):
        return self.conceptSchemas

    def get_conceptList(self):
        return self.conceptLists

    def set_context(self, context, mapping):
        self.context = context
        self.context_mapping = mapping

    def save(self, param):
        getattr(self, param).save()
