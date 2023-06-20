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
from re import search
from sdmx2jsonld.exceptions.exceptions import ClassFreqError
from sdmx2jsonld.common.commonclass import CommonClass


class Frequency(CommonClass):
    def __init__(self):
        # sdmx-dimension:freq a qb:DimensionProperty, rdf:Property;
        #    rdfs:range rdfs:Resource;
        #    qb:concept sdmx-concept:freq;
        #    rdfs:label "Frequency"@en;
        #    rdfs:comment """The time interval at which observations occur over a given time period."""@en;
        #    rdfs:isDefinedBy <https://sdmx.org/wp-content/uploads/01_sdmx_cog_annex_1_cdc_2009.pdf>.
        super().__init__(entity='DimensionProperty')
        self.data = {
            "id": "urn:ngsi-ld:DimensionProperty:freq",
            "type": "DimensionProperty",
            "dct:language": {
                "type": "Property",
                "value": ["en"]
            },
            "rdfs:label": {
                "type": "Property",
                "value": {
                    "en": "Frequency",
                }
            },
            "dct:description": {
                "type": "Property",
                "value": {
                    "en": "The time interval at which observations occur over a given time period.",
                }
            },
            "concept": {
                "type": "Relationship",
                "object": "urn:ngsi-ld:Concept:freq"
            },
            "dct:identifier": {
                "type": "Property",
                "value": "freq"
            },
            "rdfs:range": {
                "type": "Property",
                "value": "xsd:string"
            },
            "@context": {
                "sdmp": "https://smart-data-models.github.io/dataModel.STAT-DCAT-AP/context.jsonld",
                "dcat": "http://www.w3.org/ns/dcat#",
                "stat": "http://data.europa.eu/(xyz)/statdcat-ap/",
                "dct": "http://purl.org/dc/terms/",
                "qb": "http://purl.org/linked-data/cube#",
                "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
            }
        }

    @staticmethod
    def fix_value(value):
        # Need to check if the value received is in the list of possible values -> return that value
        # then maybe could be in the form freq-<value>, so we have to extract the substring and
        #      return that substring if it is in the list of values, if not return an error.
        # any other value will return an error
        value_upper = value.upper()

        m = search('FREQ-(.*)', value_upper)

        if m is not None:
            status = m.group(1)
            return status
        else:
            # We received a value that it is not following the template format
            raise ClassFreqError(value)