from transform.dataset import Dataset
from transform.dimension import Dimension


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
        self.dimensions = list()

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
        data_type, new_string = self.__find_entity_type__(string=string)

        if data_type == 'Component':
            self.dataset.add_components(component=new_string)
        elif data_type == 'Dataset':
            title = string[0].split(':')[1]
            self.dataset.add_data(title=title, data=new_string)
        elif data_type == 'Dimension':
            dimension = Dimension()
            dimension_id = string[0].split(':')[1]
            dimension.add_data(dimension_id=dimension_id, data=new_string)
            self.dimensions.append(dimension)

    def get_dataset(self):
        return self.dataset.get()

    def get_dimensions(self):
        return self.dimensions
