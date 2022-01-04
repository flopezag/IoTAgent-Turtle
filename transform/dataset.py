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
            "rdfs:label": {
                "type": "LanguageProperty",
                "LanguageMap": dict()
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
            self.attributes['stat:attribute']['value'].append(component[position][0])
        elif type_component == 'qb:dimension':
            self.dimensions['stat:dimension']['value'].append(component[position][0])
        elif type_component == 'qb:measure':
            self.unitMeasures['stat:unitMeasure']['value'].append(component[position][0])
        else:
            print(f"Error, it was identified a qb:ComponentSpecification with a wrong type: {type_component}")
            exit(-1)

    def get(self):
        self.data = self.data | self.dimensions | self.attributes | self.unitMeasures
        return self.data

    def add_data(self, title, data):
        print(data)

        # We need to complete the data corresponding to the Dataset: rdfs:label
        position = data.index('rdfs:label') + 1
        description = data[position]

        descriptions = [x[0].replace("\"", "") for x in description]
        languages = [x[1].replace("@", "").lower() for x in description]

        for i in range(0, len(languages)):
            self.data['rdfs:label']['LanguageMap'][languages[i]] = descriptions[i]

        # Complete the information of the language with the previous information
        self.data['language']['value'] = languages

        # Add the title
        self.data['title']['value'] = title

        print(self.data['rdfs:label'])
