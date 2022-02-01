from transform.property import Property

class Dimension(Property):
    def __init__(self):
        super().__init__()
        self.data['type'] = 'DimensionProperty'

    def add_data(self, id, data):
        super().add_data(id=id, data=data)

        # Add the id
        self.data['id'] = "urn:ngsi-ld:DimensionProperty:" + id
