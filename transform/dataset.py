from json import dumps
from logging import getLogger

logger = getLogger()


class Dataset:
    def __init__(self):
        self.data = {
            "id": str(),
            "type": "Dataset",
            "title": {
                "type": "Property",
                "value": str()
            },
            "language": {
                "type": "Property",
                "value": list()
            },


            #################################################
            # TODO: New ETSI CIM NGSI-LD specification 1.4.2
            # Pending to implement in the Context Broker
            #################################################
            # "rdfs:label": {
            #     "type": "LanguageProperty",
            #     "LanguageMap": dict()
            # },
            #################################################
            "description": {
                "type": "Property",
                "value": dict()
            },


            "@context": dict()
        }

        self.dimensions = {
            "stat:dimension": {
                "type": "Property",
                "value": list()
            }
        }

        self.attributes = {
            "stat:attribute": {
                "type": "Property",
                "value": list()
            }
        }

        self.unitMeasures = {
            "stat:unitMeasure": {
                "type": "Property",
                "value": list()
            }
        }

    def add_components(self, component):
        # We need to know which kind of component we have, it should be the verb:
        # qb:attribute, qb:dimension, or qb:measure
        type_component = [x for x in ['qb:attribute', 'qb:dimension', 'qb:measure'] if x in component][0]
        position = component.index(type_component) + 1

        if type_component == 'qb:attribute':
            id = self.__generate_id__(entity="AttributeProperty", value=component[position][0])
            self.attributes['stat:attribute']['value'].append(id)
        elif type_component == 'qb:dimension':
            id = self.__generate_id__(entity="DimensionProperty", value=component[position][0])
            self.dimensions['stat:dimension']['value'].append(id)
        elif type_component == 'qb:measure':
            id = self.__generate_id__(entity="Measure", value=component[position][0])
            self.unitMeasures['stat:unitMeasure']['value'].append(id)
        else:
            print(f"Error, it was identified a qb:ComponentSpecification with a wrong type: {type_component}")

    def __generate_id__(self, entity, value):
        aux = value.split(":")
        aux = "urn:ngsi-ld:" + entity + ":" + aux[len(aux)-1]
        return aux

    def get(self):
        self.data = self.data | self.dimensions | self.attributes | self.unitMeasures
        return self.data

    def add_data(self, title, data):
        # TODO: We have to control that data include the indexes that we want to search
        # We need to complete the data corresponding to the Dataset: rdfs:label
        position = data.index('rdfs:label') + 1
        description = data[position]

        descriptions = [x[0].replace("\"", "") for x in description]

        languages = list()
        try:
            languages = [x[1].replace("@", "").lower() for x in description]
        except IndexError:
            logger.warning(f'The Dataset {title} has a '
                           f'rdfs:label without language tag: {description}')

            aux = len(description)
            if aux != 1:
                logger.error(f"Dataset: there is more than 1 description ({aux}), values: {description}")
            else:
                # There is no language tag, we use by default 'en'
                languages = ['en']
                logger.warning('Dataset: selecting default language "en"')

        ###############################################################################
        # TODO: New ETSI CIM NGSI-LD specification 1.4.2
        # Pending to implement in the Context Broker
        ###############################################################################
        # for i in range(0, len(languages)):
        #     self.data['rdfs:label']['LanguageMap'][languages[i]] = descriptions[i]
        ###############################################################################
        for i in range(0, len(languages)):
            self.data['description']['value'][languages[i]] = descriptions[i]

        # Complete the information of the language with the previous information
        self.data['language']['value'] = languages

        # Add the title
        self.data['title']['value'] = title

        # Add the id
        self.data['id'] = "urn:ngsi-ld:Dataset:" + title

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
