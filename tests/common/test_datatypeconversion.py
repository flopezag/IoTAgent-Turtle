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
from unittest import TestCase
from sdmx2jsonld.common.datatypeconversion import DataTypeConversion


class Test(TestCase):
    def setUp(self):
        self.conversion = DataTypeConversion()

    def test_datetime_string_conversion_1(self):
        """
        Check if we can get a correct datetime value from a string, case 1
        """
        obtained = self.conversion.convert('"2022-01-15T08:00:00.000"', 'xsd:dateTime')
        expected = '2022-01-15T08:00:00+00:00'
        assert obtained == expected, f"\n\nDateTime was not the expected," \
                                     f"\n    got     : {obtained}" \
                                     f"\n    expected: {expected}"

    def test_int_string_conversion(self):
        """
        Check if we can get a correct integer from a string
        """
        obtained = self.conversion.convert('"2"', 'xsd:int')
        expected = 2
        assert obtained == expected, f"\n\nInteger was not the expected," \
                                     f"\n    got     : {obtained} {type(obtained)}" \
                                     f"\n    expected: {expected} {type(expected)}"

    def test_int_integer_conversion(self):
        """
        Check if we can get a correct integer from an integer
        """
        obtained = self.conversion.convert('2', 'xsd:int')
        expected = 2
        assert obtained == expected, f"\n\nInteger was not the expected," \
                                     f"\n    got     : {obtained} {type(obtained)}" \
                                     f"\n    expected: {expected} {type(expected)}"

        # # print(dataConversionType.convert(data23[0], data23[2]) + 10)
        #

    def test_boolean_conversion(self):
        """
        Check if we can convert a boolean string into its proper value
        """
        obtained = self.conversion.convert('"true"', 'xsd:boolean')
        expected = True
        assert obtained == expected, f"\n\nBoolean was not the expected," \
                                     f"\n    got     : {obtained} {type(obtained)}" \
                                     f"\n    expected: {expected} {type(expected)}"

    def test_fake_conversion(self):
        """
        Check is a fake value data launch an exception
        """
        with self.assertRaises(Exception) as error:
            _ = self.conversion.convert('"fake"', 'otraCosa')

        self.assertEqual(str(error.exception),
                         "Datatype not defined: otraCosa")

        # # Convert datetime generated into UTC format: 2021-12-21T16:18:55Z or 2021-12-21T16:18:55+00:00, ISO8601
        #
        # data5 = ['"2022-01-10T09:00:00.000"', Token('FORMATCONNECTOR', '^^'), 'xsd:dateTime']
        # print(dataConversionType.convert(data5[0], data5[2]))
        #
        # data6 = ['"2021-07-01T11:50:37.3"', Token('FORMATCONNECTOR', '^^'), 'xsd:dateTime']
        # print(dataConversionType.convert(data6[0], data6[2]))
        #
        # data7 = ['"2021-09-28T15:31:24.05"', Token('FORMATCONNECTOR', '^^'), 'xsd:dateTime']
        # print(dataConversionType.convert(data7[0], data7[2]))
        #

    def test_float_float_conversion(self):
        """
        Check if we can get a correct integer from an string
        """
        obtained = self.conversion.convert('2345.2', 'xsd:float')
        expected = 2345.2
        assert obtained == expected, f"\n\nInteger was not the expected," \
                                     f"\n    got     : {obtained} {type(obtained)}" \
                                     f"\n    expected: {expected} {type(expected)}"

    def test_float_string_conversion(self):
        """
        Check if we can get a correct integer from an integer
        """
        obtained = self.conversion.convert('"3016.9"', 'xsd:float')
        expected = 3016.9
        assert obtained == expected, f"\n\nFloat was not the expected," \
                                     f"\n    got     : {obtained} {type(obtained)}" \
                                     f"\n    expected: {expected} {type(expected)}"
