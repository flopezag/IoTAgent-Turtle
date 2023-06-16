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


class FreqConcept(CommonClass):
    def __init__(self):
        # sdmx-concept:freq a sdmx:Concept, skos:Concept;
        #   rdfs:label "Frequency"@en;
        #   rdfs:comment """The time interval at which observations occur over a given time period."""@en;
        #   rdfs:isDefinedBy <https://sdmx.org/wp-content/uploads/01_sdmx_cog_annex_1_cdc_2009.pdf>;
        #   skos:notation "urn:sdmx:org.sdmx.infomodel.conceptscheme.Concept=SDMX:CROSS_DOMAIN_CONCEPTS[1.0].FREQ";
        #   skos:inScheme sdmx-concept:cog.
        super().__init__(entity='Concept')

        self.data = {
            "id": "urn:ngsi-ld:Concept:freq",
            "type": "Concept",
            "dct:language": {
                "type": "Property",
                "value": ["en"]
            },
            "skos:inScheme": {
                "type": "Relationship",
                "object": "urn:ngsi-ld:ConceptSchema:cog"
            },
            "skos:prefLabel": {
                "type": "Property",
                "value": {
                    "en": "Frequency"
                }
            },
            "skos:notation": {
                "type": "Property",
                "value": "urn:sdmx:org.sdmx.infomodel.conceptscheme.Concept=SDMX:CROSS_DOMAIN_CONCEPTS[1.0].FREQ"
            },
            "@context": {
                "sdmp": "https://smart-data-models.github.io/dataModel.STAT-DCAT-AP/context.jsonld",
                "dcat": "http://www.w3.org/ns/dcat#",
                "stat": "http://data.europa.eu/(xyz)/statdcat-ap/",
                "dct": "http://purl.org/dc/terms/",
                "skos": "http://www.w3.org/2004/02/skos/core#"
            }
        }
