from pathlib import Path
import json
from requests import post, exceptions


class NGSILDConnector:
    def __init__(self, path=None):
        if path == None:
            config_path = Path.cwd().joinpath('common/config.json')
        else:
            config_path = Path.cwd().joinpath(path)
        config = dict()
        with open(config_path) as config_file:
            config = json.load(config_file)
        self.base_url = config['broker']

    def get_url(self):
        url = f"{self.base_url}/ngsi-ld/v1/entityOperations/create"
        return url

    def send_pretty_much_data(self, json_object):
        d = json.loads(json_object)
        d = d if type(d) is list else [d]

        for elem in d:
            rc, r = c.send_data(json.dumps(elem))
            print("Code: ", rc)
            print(r)

    def send_data(self, json_object):
        # Send the data to a FIWARE Context Broker instance
        headers = {
            'Content-Type': 'application/ld+json',
            'Accept': 'application/ld+json'
        }

        url = self.get_url()
        resp = "..."

        r = post(url=url, headers=headers, data=json_object, timeout=5)

        resp = json.loads(r.text)
        response_status_code = r.status_code

        # Let exceptions raise.... They can be controlled somewhere else.
        return response_status_code, resp


from sdmx2jsonld.transform.parser import Parser
from io import StringIO

if __name__ == "__main__":
    c = NGSILDConnector('../common/config.json')
    print(c.get_url())

    parser = Parser()
    with open("../examples/structures-tourism.ttl", "r") as rf:
        rdf_data = rf.read()

    r = parser.parsing(StringIO(rdf_data), out=False)

    with open("/tmp/ww", "w") as f:
        f.write(r)

    # print(data)
    c.send_pretty_much_data(r)
    # rc, r = c.send_data(data)
    # print("Code: ", rc)
    # print(r)
