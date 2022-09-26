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

logger = getLogger()


class DataRange:
    def __init__(self):
        self.notation = str()
        self.labels = dict()
        self.id = str()

    def add_data(self, range_id, data):
        # TODO: We have to control that data include the indexes that we want to search
        # We need to complete the data corresponding to the Range: skos:prefLabel
        try:
            position = data.index('skos:prefLabel') + 1
        except ValueError:
            # We could not find skos:prefLabel, try to find rdfs:label
            position = data.index('rdfs:label') + 1
            logger.warning(f'The Range {range_id} does not contain skos:prefLabel but rdfs:label. We use its '
                           f'content to fill in the skos:prefLabel property')

        description = data[position]
        descriptions = [x[0].replace("\"", "") for x in description]

        languages = list()
        try:
            languages = [x[1].replace("@", "").lower() for x in description]
        except IndexError:
            logger.warning(f'The Range {range_id} has a '
                           f'skos:prefLabel without language tag: {description}')

            aux = len(description)
            if aux != 1:
                logger.error(f"Range: there is more than 1 description ({aux}), values: {description}")
            else:
                # There is no language tag, we use by default 'en'
                languages = ['en']
                logger.warning('Range: selecting default language "en"')

        # Complete the skos:prefLabel
        for i in range(0, len(languages)):
            self.labels[languages[i]] = descriptions[i]

        # skos:notation
        position = data.index('skos:notation') + 1
        self.notation = data[position][0][0].replace("\"", "")

        # Complete the id
        self.id = data[0]
