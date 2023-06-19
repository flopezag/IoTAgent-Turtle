from unittest import TestCase
from sdmx2jsonld.common.listmanagement import get_rest_data, flatten_value

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

