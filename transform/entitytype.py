from transform.dataset import Dataset
from transform.dimension import Dimension
from transform.conceptschema import ConceptSchema
from transform.concept import Concept
from transform.datarange import DataRange
from transform.attribute import Attribute


class EntityType:
    def __init__(self):
        self.entities = {
            'qb:DataStructureDefinition': 'Dataset',
            'qb:ComponentSpecification': 'Component',
            'qb:AttributeProperty': 'Attribute',
            'qb:DimensionProperty': 'Dimension',
            'rdfs:Class': 'Class',
            'owl:Class': 'Class',
            'skos:ConceptScheme': 'ConceptScheme',
            'skos:Concept': 'Range'
        }

        self.dataset = Dataset()
        self.dimensions = list()
        self.attributes = list()
        self.conceptSchemas = list()
        self.conceptLists = list()
        self.conceptListsIds = dict()
        self.context = dict()

    def __find_entity_type__(self, string):
        """
        Find the index position of the 'a' SDMX key and return the following data with the corresponding EntityType
        """
        # Index maybe 0 in case of ComponentSpecification or 1 in case of DataStructureDefinition
        index = len(string) - 1
        string = string[index]

        position = string.index('a') + 1
        # data = string[position][0]
        data = string[position][len(string[position]) - 1]

        # We have two options, a well know object list to be found in the self.entities or
        # the conceptList defined in the turtle file
        try:
            data = self.entities[data]
        except KeyError:
            # We found a CodeList or any other thing, check the list of codeList found in the turtle file
            if data not in self.conceptListsIds:
                print(f"Received a unexpected entity type: {data}")
            else:
                data = 'Range'

        return data, string

    def transform(self, string, context):
        data_type, new_string = self.__find_entity_type__(string=string)

        if data_type == 'Component':
            self.dataset.add_components(component=new_string)
        elif data_type == 'Dataset':
            title = string[0].split(':')[1]
            self.dataset.add_data(title=title, data=new_string)
            self.dataset.add_context(context=context)
        elif data_type == 'Dimension':
            dimension = Dimension()
            dimension_id = string[0].split(':')[1]
            dimension.add_data(id=dimension_id, data=new_string)
            dimension.add_context(context=context)
            self.dimensions.append(dimension)
        elif data_type == 'Attribute':
            attribute = Attribute()
            attribute_id = string[0].split(':')[1]
            attribute.add_data(id=attribute_id, data=new_string)
            attribute.add_context(context=context)
            self.attributes.append(attribute)
        elif data_type == 'ConceptScheme':
            conceptSchema = ConceptSchema()

            if ':' in string[0]:
                aux = string[0].split(':')[1]
                aux = aux.split('/')
                conceptSchemaId = '_'.join(aux[len(aux)-2:])
            else:
                conceptSchemaId = string[0]

            conceptSchema.add_data(concept_schema_id=conceptSchemaId, data=new_string)
            conceptSchema.add_context(context=context)
            self.conceptSchemas.append(conceptSchema)
        elif data_type == 'Class':
            # We need the Concept because each of the Range description is of the type Concept
            conceptList = Concept()
            conceptlistId = string[0].split(':')[1]
            conceptList.add_data(conceptId=conceptlistId, data=new_string)
            conceptList.add_context(context=context)
            self.conceptLists.append(conceptList)
            self.conceptListsIds[string[0]] = conceptList.get_id()
        elif data_type == 'Range':
            data_range = DataRange()
            data_range_id = string[0].split(':')[1].split('/')
            data_range_id = data_range_id[len(data_range_id)-1]
            data_range.add_data(range_id=data_range_id, data=string)

            for i in range(0, len(self.conceptSchemas)):
                concept_schema = self.conceptSchemas[i].data
                has_top_concept_values = concept_schema['skos:hasTopConcept']['value']

                out = [data_range.notation if x == data_range.id else x for x in has_top_concept_values]

                self.conceptSchemas[i].data['skos:hasTopConcept']['value'] = out

    def get_dataset(self):
        return self.dataset.get()

    def get_dimensions(self):
        return self.dimensions

    def get_attributes(self):
        return self.attributes

    def get_conceptSchemas(self):
        return self.conceptSchemas

    def get_conceptList(self):
        return self.conceptLists

    def save(self, param):
        getattr(self, param).save()
