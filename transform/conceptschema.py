class ConceptSchema:
    def __init__(self):
        self.data = {
            "id": str(),
            "type": "skos:ConceptScheme",
            "skos:hasTopConcept": {
                "type": "Property",
                "value": list()
            },


            #################################################
            # TODO: New ETSI CIM NGSI-LD specification 1.4.2
            # Pending to implement in the Context Broker
            #################################################
            # "skos:prefLabel": {
            #     "type": "LanguageProperty",
            #     "LanguageMap": dict()
            # },
            #################################################
            "skos:prefLabel": {
                "type": "Property",
                "value": dict()
            },


            "@context": dict()
        }

    def add_data(self, concept_schema_id, data):
        # TODO: We have to control that data include the indexes that we want to search
        # We need to complete the data corresponding to the ConceptSchema: skos:prefLabel
        position = data.index('skos:prefLabel') + 1
        description = data[position]

        descriptions = [x[0].replace("\"", "") for x in description]
        languages = list()
        try:
            languages = [x[1].replace("@", "").lower() for x in description]
        except IndexError:
            print(f"\nThe ConceptSchema {concept_schema_id} has a skos:prefLabel without languages: {descriptions}\n\n")

        # Complete the skos:prefLabel
        ###############################################################################
        # TODO: New ETSI CIM NGSI-LD specification 1.4.2
        # Pending to implement in the Context Broker
        ###############################################################################
        # for i in range(0, len(languages)):
        #     self.data['skos:prefLabel']['LanguageMap'][languages[i]] = descriptions[i]
        ###############################################################################
        for i in range(0, len(languages)):
            self.data['skos:prefLabel']['value'][languages[i]] = descriptions[i]

        # Add the id
        self.data['id'] = "urn:ngsi-ld:ConceptSchema:" + concept_schema_id

        # skos:hasTopConcept, this is a list of ids
        position = data.index('skos:hasTopConcept') + 1
        self.data['skos:hasTopConcept']['value'] = data[position]

    def get(self):
        return self.data

    def add_context(self, context):
        # TODO: We should assign only the needed context and not all the contexts
        self.data['@context'] = context['@context']
