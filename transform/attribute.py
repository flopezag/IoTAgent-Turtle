from transform.property import Property


class Attribute(Property):
    def __init__(self):
        super().__init__()
        self.data['type'] = 'AttributeProperty'

    def add_data(self, id, data):
        super().add_data(id=id, data=data)

        # Add the id
        self.data['id'] = "urn:ngsi-ld:AttributeProperty:" + id
