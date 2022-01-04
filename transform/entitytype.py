from transform.dataset import Dataset


class EntityType:
    def __init__(self):
        self.entities = {
            'qb:DataStructureDefinition': 'Dataset',
            'qb:ComponentSpecification': 'Component',
            'qb:CodedProperty': 'Dimension',
            'qb:DimensionProperty': 'Dimension',
            'rdfs:Class': '...',
            'skos:ConceptScheme': '...',
            'skos:Concept': '...',
            'isc:age': '...',  # Problem with this...
            'isc:sex': '...',
            'isc:lau': '...'
        }

        self.dataset = Dataset()

    def __find_entity_type__(self, string):
        """
        Find the index position of the 'a' SDMX key and return the following data with the corresponding EntityType
        """
        # Index maybe 0 in case of ComponentSpecification or 1 in case of DataStructureDefinition
        index = len(string) - 1
        string = string[index]

        position = string.index('a') + 1
        data = string[position][0]
        data = self.entities[data]

        return data, string

    def transform(self, string):
        data_type, string = self.__find_entity_type__(string=string)

        if data_type == 'Component':
            self.dataset.add_component(component=string)

    def get_dataset(self):
        return self.dataset.get()



