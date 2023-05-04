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


def filter_key_with_prefix(prefix_key, not_allowed_keys, further_process_keys):
    aux = prefix_key.split(":")

    # We dismiss the following keys to be analysed due to they are not manage in the current version of
    # statDCAT-AP (sliceKey, disseminationStatus, validationState, notation), they are manage in a separate
    # process (label) or manage afterward analysing the turtle file (component)
    # TODO: we should keep component in order to check that afterwards we get the definition of that component
    if len(aux) == 2:
        if aux[1] not in not_allowed_keys:
            # this is a key with prefix that we want to keep
            return True
        else:
            if aux[1] not in ['component', 'label']:
                # These are the identified not allowed keys, we need to inform about them
                logger.warning(f'The property {aux[1]} is not supported in statDCAT-AP')
            else:
                # These are the identified keys managed in a different way
                logger.info(f'The property {aux[1]} is manage afterwards in Dataset Class or in Property Class')

            return False
    else:
        return False


def flatten_value(y):
    if isinstance(y, list):
        aux = len(y)
        if aux == 1:
            return flatten_value(y[0])
        elif aux > 1:
            # for each element of the list we have to flatten to string and create the corresponding list
            # We need to differentiate between multilingual case and multiple data
            # this case corresponds to multilingual content
            if len(y[0]) == 2:
                # Multilingual case
                result = dict()
                for i in range(0, aux):
                    result[y[i][1][1:]] = flatten_value(y[i][0])
            else:
                # Normal case
                result = list()
                for i in range(0, aux):
                    result.append(flatten_value(y[i]))
            return result
        else:  # in case of len == 0 be return the empty string
            return ''
    else:
        return y.replace('"', '')


def get_rest_data(data, not_allowed_keys=[], further_process_keys=[]):
    aux = {data[i]: flatten_value(data[i + 1]) for i in range(0, len(data), 2)}

    # We need to get the list of keys from the dict
    new_keys = list(
        filter(lambda x: filter_key_with_prefix(x, not_allowed_keys, further_process_keys), list(aux.keys())))

    new_data = {k: aux[k] for k in new_keys}

    return new_data
