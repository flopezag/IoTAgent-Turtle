from transform.property import Property


class Attribute(Property):
    def __init__(self):
        super().__init__()
        self.data['type'] = 'AttributeProperty'

    def add_data(self, id, data):
        super().add_data(id=id, data=data)

        # Add the id
        self.data['id'] = "urn:ngsi-ld:AttributeProperty:" + id

    # def add_context(self, context):
    #     super().add_context(context=context)
    #
    # def get(self):
    #     return self.data
    #
    # def save(self):
    #     data = self.get()
    #
    #     aux = data['id'].split(":")
    #     length_aux = len(aux)
    #     filename = '_'.join(aux[length_aux - 2:]) + '.jsonld'
    #
    #     # Serializing json
    #     json_object = dumps(data, indent=4, ensure_ascii=False)
    #
    #     # Writing to sample.json
    #     with open(filename, "w") as outfile:
    #         outfile.write(json_object)
