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
from sdmx2jsonld.sdmxattributes.exceptions import ClassObsStatusError
from sdmx2jsonld.common.commonclass import CommonClass


class ObsStatus(CommonClass):
    status: list() = [
        "A",
        "B",
        "D",
        "E",
        "F",
        "G",
        "I",
        "K",
        "W",
        "O",
        "M",
        "P",
        "S",
        "L",
        "H",
        "Q",
        "J",
        "N",
        "U",
        "V"
    ]

    def __init__(self):
        # sdmx-attribute:obsStatus a qb:AttributeProperty, rdf:Property  ;
        #     qb:concept sdmx-concept:obsStatus ;
        #     rdfs:label "Observation Status"@en ;
        #     rdfs:comment """Information on the quality of a value or an unusual or missing value."""@en ;
        #     rdfs:isDefinedBy <https://sdmx.org/wp-content/uploads/01_sdmx_cog_annex_1_cdc_2009.pdf> .
        super().__init__(entity='AttributeProperty')
        self.data = {
            "id": "urn:ngsi-ld:AttributeProperty:obsStatus",
            "type": "AttributeProperty",
            "dct:language": {
                "type": "Property",
                "value": ["en"]
            },
            "rdfs:label": {
                "type": "Property",
                "value": {
                    "en": "Observation Status",
                }
            },
            "dct:description": {
                "type": "Property",
                "value": {
                    "en": "Information on the quality of a value or an unusual or missing value.",
                }
            },
            "concept": {
                "type": "Relationship",
                "object": "urn:ngsi-ld:Concept:obsStatus"
            },
            "dct:identifier": {
                "type": "Property",
                "value": "obsStatus"
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

    def fix_value(self, value):
        # Need to check if the value received is in the list of possible values -> return that value
        # then maybe could be in the form obsStatus-<value>, so we have to extract the substring and
        #      return that substring if it is in the list of values, if not return an error.
        # any other value will return an error
        value_upper = value.upper()

        if value_upper in self.status:
            return value_upper
        else:
            # we could receive a value in the format obsStatus-<value>
            m = search('OBSSTATUS-(.*)', value_upper)

            if m is not None:
                status = m.group(1)

                if status in self.status:
                    return status
                else:
                    message = f"ObsStatus value is not included in the list of available values,\n" \
                              f"    got:{value}\n" \
                              f"    expected:{['obsStatus-'+x for x in self.status]}"

                    raise ClassObsStatusError(data=value, message=message)

            else:
                # We received a value that it is not following the template format
                raise ClassObsStatusError(value)
