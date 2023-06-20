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
        url = f"{self.base_url}/ngsi-ld/v1/entities"
        return url

    def send_data_array(self, json_object):
        return_info = []
        d = json.loads(json_object)
        d = d if type(d) is list else [d]

        for elem in d:
            try:
                rc, r = self.send_data(json.dumps(elem))
                return_info.append({"id": elem['id'],
                                   "status_code": rc,
                                   "reason": r})
            except TypeError as e:
                return_info.append({"id": "UNK",
                                    "status_code": 500,
                                    "reason": e.args[0]})
            except Exception as e:
                raise e
                # reason = getattr(e, 'message', str(e))
                # return_info.append({"id": "UNK",
                #                     "status_code": 500,
                #                    "reason": reason})

        return return_info


    def send_data(self, json_object):
        # Send the data to a FIWARE Context Broker instance
        headers = {
            'Content-Type': 'application/ld+json'
            #, 'Accept': 'application/ld+json'
        }

        url = self.get_url()
        resp = "..."

        r = post(url=url, headers=headers, data=json_object, timeout=5)

        # resp = json.loads(r.text)
        response_status_code = r.status_code

        if response_status_code == 201:
            print("LOCATION: ", r.headers['Location'])

        # Let exceptions raise.... They can be controlled somewhere else.
        return response_status_code, r.reason


from sdmx2jsonld.transform.parser import Parser
from io import StringIO

if __name__ == "__main__":
    c = NGSILDConnector('../common/config.json')
    print(c.get_url())

    parser = Parser()
    with open("../examples/structures-tourism.ttl", "r") as rf:
        rdf_data = rf.read()

    r = parser.parsing(StringIO(rdf_data), out=False)
    c.send_data_array(r)
