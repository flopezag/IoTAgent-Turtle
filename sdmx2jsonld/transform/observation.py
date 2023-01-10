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
from sdmx2jsonld.sdmxattributes.confirmationStatus import ConfStatus
from sdmx2jsonld.sdmxattributes.observationStatus import ObsStatus
from re import search

logger = getLogger()


class Observation(CommonClass):
    def __init__(self):
        super().__init__(entity='Observation')

        self.data = {
            "id": str(),
            "type": "Observation",
            "title": {
                "type": "Property",
                "value": str()
            },
            "identifier": {
                "type": "Property",
                "value": str()
            },
            "dataSet": {
                "type": "Property",
                "object": str()
            },
            "confStatus": {
                "type": "Property",
                "value": str()
            },
            "decimals": {
                "type": "Property",
                "value": int()
            },
            "obsStatus": {
                "type": "Property",
                "value": str()
            },
            "unitMult": {
                "type": "Property",
                "value": int()
            },
            "freq": {
                "type": "Property",
                "value": str()
            },
            "refArea": {
                "type": "Property",
                "value": str()
            },
            "timePeriod": {
                "type": "Property",
                "value": str()
            },
            "obsValue": {
                "type": "Property",
                "value": float()
            },
            "dimensions": {
                "type": "Property",
                "value": list()
            },
            "@context": [
                "https://raw.githubusercontent.com/smart-data-models/dataModel.SDMX/master/context.jsonld"
            ]
        }

        self.concept_id = str()
        self.keys = {k: k for k in self.data.keys()}

    def add_data(self, title, observation_id, data):
        # We have a list of dimensions, a dataset, a list of attributes, a list of dimensions attributes
        # and an observation

        # Add the confStatus
        key = self.__assign_property__(requested_key='sdmx-attribute:confStatus', data=data)
        self.data[key]['value'] = ConfStatus().fix_value(value=self.data[key]['value'])

        # Add the id
        self.data['id'] = "urn:ngsi-ld:Observation:" + observation_id

        # Add the decimals
        self.__assign_property__(requested_key='sdmx-attribute:decimals', data=data)

        # Add obsStatus
        key = self.__assign_property__(requested_key='sdmx-attribute:obsStatus', data=data)
        self.data[key]['value'] = ObsStatus().fix_value(value=self.data[key]['value'])

        # Add unitMult
        self.__assign_property__(requested_key='sdmx-attribute:unitMult', data=data)

    def __assign_property__(self, requested_key, data):
        key = self.get_key(requested_key=requested_key)
        position = data.index(requested_key) + 1
        self.data[key]['value'] = data[position][0]

        return key

    def get_key(self, requested_key):
        try:
            key = self.keys[requested_key]
            return key
        except KeyError:
            # The key did not exist therefore we add to the list with this value
            # We need to check if it exists without prefix
            m = search('(.*):(.*)', requested_key)

            if m is not None:
                prefix = m.group(1)
                subfix = m.group(2)

                try:
                    key = self.keys[subfix]
                    return key
                except KeyError:
                    # Even subfix is not in the list, decide to add to the list of keys
                    self.keys[requested_key] = requested_key
                    return requested_key
            else:
                # Weird situation, it is an key without prefix and not recognised, decide to add it
                self.keys[requested_key] = requested_key

                return requested_key

    def get(self):
        return self.data
