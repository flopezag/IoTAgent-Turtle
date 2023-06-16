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
from sdmx2jsonld.sdmxattributes.exceptions import ClassFreqError
from sdmx2jsonld.common.commonclass import CommonClass


class RefArea(CommonClass):
    def __init__(self):
        # sdmx-dimension:refArea a qb:DimensionProperty, rdf:Property;
        #   rdfs:range rdfs:Resource;
        #   qb:concept sdmx-concept:refArea;
        #   rdfs:label "Reference Area"@en;
        #   rdfs:comment "The country or geographic area to which the measured statistical phenomenon relates."@en;
        #   rdfs:isDefinedBy <https://sdmx.org/wp-content/uploads/01_sdmx_cog_annex_1_cdc_2009.pdf>.
        super().__init__(entity='DimensionProperty')
        self.data = {
            "id": "urn:ngsi-ld:DimensionProperty:refArea",
            "type": "DimensionProperty",
            "dct:language": {
                "type": "Property",
                "value": ["en"]
            },
            "rdfs:label": {
                "type": "Property",
                "value": {
                    "en": "Reference Area",
                }
            },
            "dct:description": {
                "type": "Property",
                "value": {
                    "en": "The country or geographic area to which the measured statistical phenomenon relates.",
                }
            },
            "conceptDefinedBy": {
                "type": "Property",
                "value": "https://raw.githubusercontent.com/UKGovLD/publishing-statistical-data/master/specs/src/main"
                         "/vocab/sdmx-concept.ttl"
            },
            "isDefinedBy": {
                "type": "Property",
                "value": "https://sdmx.org/wp-content/uploads/01_sdmx_cog_annex_1_cdc_2009.pdf"
            },
            "dct:identifier": {
                "type": "Property",
                "value": "refArea"
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
