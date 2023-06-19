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
from sdmx2jsonld.exceptions.exceptions import ClassConfStatusError
from sdmx2jsonld.common.commonclass import CommonClass


class SDMXAttribute(CommonClass):
    def __init__(self, entity_id, label, description, concept_id, identifier, entity_range):
        super().__init__(entity='AttributeProperty')
        self.data = {
            "id": f"urn:ngsi-ld:AttributeProperty:{entity_id}",
            "type": "AttributeProperty",
            "dct:language": {
                "type": "Property",
                "value": ["en"]
            },
            "rdfs:label": {
                "type": "Property",
                "value": {
                    "en": label,
                }
            },
            "dct:description": {
                "type": "Property",
                "value": {
                    "en": description,
                }
            },
            "concept": {
                "type": "Relationship",
                "object": f"urn:ngsi-ld:Concept:{concept_id}"
            },
            "dct:identifier": {
                "type": "Property",
                "value": identifier
            },
            "rdfs:range": {
                "type": "Property",
                "value": entity_range
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
