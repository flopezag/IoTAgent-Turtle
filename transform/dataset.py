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
            "description": {
                "type": "Property",
                "value": list()
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

    def add_component(self, component):
        # We need to know which kind of component we have, it should be the verb:
        # qb:attribute, qb:dimension, or qb:measure
        type = [x for x in ['qb:attribute', 'qb:dimension', 'qb:measure'] if x in component][0]
        position = component.index(type) + 1

        if type == 'qb:attribute':
            self.attributes['stat:attribute']['value'].append(component[position])
        elif type == 'qb:dimension':
            self.dimensions['stat:dimension']['value'].append(component[position])
        elif type == 'qb:measure':
            self.unitMeasures['stat:unitMeasure']['value'].append(component[position])
        else:
            print(f"Error, it was identified a qb:ComponentSpecification with a wrong type: {type}")
            exit(-1)

    def get(self):
        self.data = self.data | self.dimensions | self.attributes | self.unitMeasures
        return self.data


if __name__ == '__main__':
    a = Dataset()

    # a.print_context()
    # a.add_context({'rdf': '<http://www.w3.org/1999/02/22-rdf-syntax-ns#>'})
    # a.print_context()
