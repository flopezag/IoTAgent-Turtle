from unittest import TestCase
from sdmx2jsonld.transform.parser import Parser
from io import StringIO
import os, shutil

class TestCommonClass(TestCase):
    def setUp(self) -> None:
        pass

    def clean_output_dir(self) -> None:
        for a in os.listdir("output"):
            file_path = os.path.join("output", a)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print("----------------------------")
                print(e.message)
                print("----------------------------")

    def test_file_1(self):
        for a in ["observation.ttl", "structures-accounts.ttl", "structures-tourism.ttl"]:
            print(f"Parsing: {a}")
            parser = Parser()
            with open(f"../../examples/{a}", "r") as rf:
                rdf_data = rf.read()
            r = parser.parsing(content=StringIO(rdf_data), out=False)

    def test_file_2(self):
        for a in ["observation.ttl", "structures-accounts.ttl", "structures-tourism.ttl"]:
            self.clean_output_dir()
            parser = Parser()
            r = parser.parsing(content=open(f"../../examples/{a}", "r"), out=True)

    def test_file_3(self):
        for a in ["observation.ttl", "structures-accounts.ttl", "structures-tourism.ttl"]:
            parser = Parser()
            r = parser.parsing(content=open(f"../../examples/{a}", "r"), out=False)
