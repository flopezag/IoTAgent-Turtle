from unittest import TestCase
from sdmx2jsonld.common.listmanagement import get_rest_data, flatten_value, extract_prefix
from sdmx2jsonld.exceptions.exceptions import ClassExtractPrefixError

class TestRegToParser(TestCase):
    def setUp(self) -> None:
        pass

    def test_get_rest_data(self):
        data = ['a', ['qb:AttributeProperty'], 'rdfs:label', [['"SDMX attribute COMMENT_OBS"', '@en'], ['"Attribut SDMX "', '@fr']], 'dct:created', [['2022-01-15T06:00:00+00:00']], 'dct:identifier', [['"a3003"']], 'dct:modified', [['2022-01-15T06:30:00+00:00']], 'qb:concept', ['http://bauhaus/concepts/definition/c4303'], 'insee:disseminationStatus', ['http://id.insee.fr/codes/base/statutDiffusion/Prive'], 'insee:validationState', [['"Unpublished"']], 'rdfs:range', ['xsd:string'], 'skos:notation', [['"COMMENT_OBS"']]]
        not_allowed_keys = ['sliceKey', 'component', 'disseminationStatus', 'validationState', 'notation', 'label', 'codeList', 'concept']
        further_process_keys = ['component', 'label']
        expected_res = {'dct:created': '2022-01-15T06:00:00+00:00', 'dct:identifier': 'a3003', 'dct:modified': '2022-01-15T06:30:00+00:00', 'rdfs:range': 'xsd:string'}
        res = get_rest_data(data, not_allowed_keys, further_process_keys)
        assert(expected_res == res)

    def test_flatten_value(self):
        data = [['"SDMX attribute PRE_BREAK_VALUE"', '@en'], ['"Attribut SDMX "', '@fr']]
        expected_res = {'en': 'SDMX attribute PRE_BREAK_VALUE', 'fr': 'Attribut SDMX '}
        got_data = flatten_value(data)
        assert(got_data == expected_res)

    # data = ['', None, 'dct:created', 'dct:identifier', 'dct:modified', 'rdfs:range', 'uno', 'a:b:c']
    def test_extract_prefix_with_a_prefix(self):
        data = 'a:b'
        expected_res = 'b'
        got_res = extract_prefix(data)
        assert(got_res == expected_res)

    def test_extract_prefix_with_several_prefixes(self):
        data = 'a:b:c'
        expected = "Unexpected number of prefixes: 'a:b:c'"
        with self.assertRaises(ClassExtractPrefixError) as error:
            _ = extract_prefix(attribute=data)

        self.assertEqual(str(error.exception.message), expected)

    def test_extract_prefix_with_None_value(self):
        data = None
        expected = "Unexpected data received: 'None'"
        with self.assertRaises(ClassExtractPrefixError) as error:
            _ = extract_prefix(attribute=data)

        self.assertEqual(str(error.exception.message), expected)

    def test_extract_prefix_with_empty_value(self):
        data = ''
        expected = "Unexpected data received: ''"
        with self.assertRaises(ClassExtractPrefixError) as error:
            _ = extract_prefix(attribute=data)

        self.assertEqual(str(error.exception.message), expected)

    def test_extract_prefix_with_a_value_without_prefix(self):
        data = 'a'
        expected_res = 'a'
        got_res = extract_prefix(data)
        assert(got_res == expected_res)
