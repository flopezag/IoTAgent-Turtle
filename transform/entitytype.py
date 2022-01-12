from transform.dataset import Dataset
from transform.dimension import Dimension
from transform.conceptschema import ConceptSchema
from transform.codelist import CodeList
from transform.datarange import DataRange


class EntityType:
    def __init__(self):
        self.entities = {
            'qb:DataStructureDefinition': 'Dataset',
            'qb:ComponentSpecification': 'Component',
            'qb:CodedProperty': 'Dimension',
            'qb:DimensionProperty': 'Dimension',
            'rdfs:Class': 'Class',
            'owl:Class': 'Class',
            'skos:ConceptScheme': 'ConceptScheme',
            'skos:Concept': 'Range'
        }

        self.dataset = Dataset()
        self.dimensions = list()
        self.concept_schemas = list()
        self.codeLists = list()
        self.codeListIds = dict()

    def __find_entity_type__(self, string):
        """
        Find the index position of the 'a' SDMX key and return the following data with the corresponding EntityType
        """
        # Index maybe 0 in case of ComponentSpecification or 1 in case of DataStructureDefinition
        index = len(string) - 1
        string = string[index]

        position = string.index('a') + 1
        data = string[position][0]

        # We have two options, a well know object list to be found in the self.entities or
        # the codelist defined in the turtle file
        try:
            data = self.entities[data]
        except KeyError:
            # We found a CodeList or any other thing, check the list of codeList found in the turtle file
            if data not in self.codeListIds:
                print(f"Received a unexpected entity type: {data}")
            else:
                data = 'Range'

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
        elif data_type == 'ConceptScheme':
            concept_schema = ConceptSchema()
            concept_schema_id = string[0].split(':')[1]
            concept_schema.add_data(concept_schema_id=concept_schema_id, data=new_string)
            self.concept_schemas.append(concept_schema.get())
        elif data_type == 'Class':
            code_list = CodeList()
            code_list_id = string[0].split(':')[1]
            code_list.add_data(code_list_id=code_list_id, data=new_string)
            self.codeLists.append(code_list.get())
            self.codeListIds[string[0]] = code_list.get_id()
        elif data_type == 'Range':
            data_range = DataRange()
            data_range.add_data(range_id=data_type, data=string)

            for i in range(0, len(self.concept_schemas)):
                concept_schema = self.concept_schemas[i]
                has_top_concept_values = concept_schema['skos:hasTopConcept']['value']

                out = [data_range.notation if x == data_range.id else x for x in has_top_concept_values]

                self.concept_schemas[i]['skos:hasTopConcept']['value'] = out

    def get_dataset(self):
        return self.dataset.get()

    def get_dimensions(self):
        return self.dimensions

    def get_concept_schemas(self):
        return self.concept_schemas

    def get_code_lists(self):
        return self.codeLists
