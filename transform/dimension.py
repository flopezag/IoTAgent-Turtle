from json import dumps


class Dimension:
    def __init__(self):
        self.data = {
            "id": str(),
            "type": "DimensionProperty",


            #################################################
            # TODO: New ETSI CIM NGSI-LD specification 1.4.2
            # Pending to implement in the Context Broker
            #################################################
            # "rdfs:label": {
            #     "type": "LanguageProperty",
            #     "LanguageMap": dict()
            # },
            #################################################
            "rdfs:label": {
                "type": "Property",
                "value": dict()
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
        # TODO: We have to control that data include the indexes that we want to search
        # We need to complete the data corresponding to the Dimension: rdfs:label
        position = data.index('rdfs:label') + 1
        description = data[position]

        descriptions = [x[0].replace("\"", "") for x in description]
        languages = [x[1].replace("@", "").lower() for x in description]

        ###############################################################################
        # TODO: New ETSI CIM NGSI-LD specification 1.4.2
        # Pending to implement in the Context Broker
        ###############################################################################
        # for i in range(0, len(languages)):
        #     self.data['rdfs:label']['LanguageMap'][languages[i]] = descriptions[i]
        ###############################################################################
        for i in range(0, len(languages)):
            self.data['rdfs:label']['value'][languages[i]] = descriptions[i]

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


    def add_context(self, context):
        # TODO: We should assign only the needed context and not all the contexts
        self.data['@context'] = context['@context']

    def get(self):
        return self.data

    def save(self):
        data = self.get()

        aux = data['id'].split(":")
        length_aux = len(aux)
        filename = '_'.join(aux[length_aux - 2:]) + '.jsonld'

        # Serializing json
        json_object = dumps(data, indent=4, ensure_ascii=False)

        # Writing to sample.json
        with open(filename, "w") as outfile:
            outfile.write(json_object)
