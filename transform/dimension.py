class Dimension:
    def __init__(self):
        self.data = {
            "id": str(),
            "type": list(),
            "rdfs:label": {
                "type": "LanguageProperty",
                "LanguageMap": dict()
            },
            "qb:codeList": {
                "type": "Relationship",
                "value": str()
            },
            "qb:concept": {
                "type": "Property",
                "value": str()
            },
            "@context": dict()
        }

    def add_data(self, dimension_id, data):
        # We need to complete the data corresponding to the Dimension: rdfs:label
        position = data.index('rdfs:label') + 1
        description = data[position]

        descriptions = [x[0].replace("\"", "") for x in description]
        languages = [x[1].replace("@", "").lower() for x in description]

        for i in range(0, len(languages)):
            self.data['rdfs:label']['LanguageMap'][languages[i]] = descriptions[i]

        # Add the id
        self.data['id'] = "urn:ngsi-ld:DimensionProperty:" + dimension_id

        # qb:codeList
        position = data.index('qb:codeList') + 1
        code_list = data[position][0]
        self.data['qb:codeList']['value'] = code_list

        # qb:concept
        position = data.index('qb:concept') + 1
        concept = data[position][0]
        self.data['qb:concept']['value'] = concept

    def get(self):
        return self.data
