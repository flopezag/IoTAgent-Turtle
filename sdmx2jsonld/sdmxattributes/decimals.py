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
from sdmx2jsonld.sdmxattributes.sdmxattribute import SDMXAttribute


class Decimals(SDMXAttribute):
    def __init__(self):
        # sdmx-attribute:decimals a qb:AttributeProperty, rdf:Property  ;
        #     qb:concept sdmx-concept:decimals ;
        #     rdfs:label "Decimals"@en ;
        #     rdfs:comment """The number of digits of an observation to the right of a decimal point."""@en ;
        #     rdfs:isDefinedBy <https://sdmx.org/wp-content/uploads/01_sdmx_cog_annex_1_cdc_2009.pdf> .
        # super().__init__(entity='AttributeProperty')
        super().__init__(entity_id='decimals',
                         label='Decimals',
                         description='The number of digits of an observation to the right of a decimal point.',
                         concept_id='decimals',
                         identifier='decimals',
                         entity_range='xsd:integer')
        # self.data = {
        #     "id": "urn:ngsi-ld:AttributeProperty:decimals",
        #     "type": "AttributeProperty",
        #     "dct:language": {
        #         "type": "Property",
        #         "value": ["en"]
        #     },
        #     "rdfs:label": {
        #         "type": "Property",
        #         "value": {
        #             "en": "Decimals",
        #         }
        #     },
        #     "dct:description": {
        #         "type": "Property",
        #         "value": {
        #             "en": "The number of digits of an observation to the right of a decimal point.",
        #         }
        #     },
        #     "concept": {
        #         "type": "Relationship",
        #         "object": "urn:ngsi-ld:Concept:decimals"
        #     },
        #     "dct:identifier": {
        #         "type": "Property",
        #         "value": "decimals"
        #     },
        #     "rdfs:range": {
        #         "type": "Property",
        #         "value": "xsd:integer"
        #     },
        #     "@context": {
        #         "sdmp": "https://smart-data-models.github.io/dataModel.STAT-DCAT-AP/context.jsonld",
        #         "dcat": "http://www.w3.org/ns/dcat#",
        #         "stat": "http://data.europa.eu/(xyz)/statdcat-ap/",
        #         "dct": "http://purl.org/dc/terms/",
        #         "qb": "http://purl.org/linked-data/cube#",
        #         "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
        #     }
        # }
