from json import dumps
from logging import getLogger

logger = getLogger()

class ConceptSchema:
    def __init__(self):
        self.data = {
            "id": str(),
            "type": "ConceptScheme",
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
            logger.warning(f'The ConceptSchema {concept_schema_id} has a '
                           f'skos:prefLabel without language tag: {description}')

            aux = len(description)
            if aux != 1:
                logger.error(f"ConceptSchema: there is more than 1 description ({aux}), values: {description}")
            else:
                # There is no language tag, we use by default 'en'
                languages = ['en']
                logger.warning('ConceptSchema: selecting default language "en"')

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
