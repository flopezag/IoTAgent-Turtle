from unittest import TestCase
from sdmx2jsonld.common.regparser import RegParser
class TestRegToParser(TestCase):
    def setUp(self) -> None:
        pass

    def test_get_id(self):
        re = RegParser()
        assert(re.obtain_id("https://elmundo.es/episode-one") == "episode-one")


