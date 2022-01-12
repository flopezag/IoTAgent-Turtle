class DataRange:
    def __init__(self):
        self.notation = str()
        self.labels = dict()
        self.id = str()

    def add_data(self, range_id, data):
        # TODO: We have to control that data include the indexes that we want to search
        # We need to complete the data corresponding to the Range: skos:prefLabel
        position = data[1].index('skos:prefLabel') + 1
        description = data[1][position]

        descriptions = [x[0].replace("\"", "") for x in description]
        languages = list()
        try:
            languages = [x[1].replace("@", "").lower() for x in description]

            # Complete the skos:prefLabel
            for i in range(0, len(languages)):
                self.labels[languages[i]] = descriptions[i]
        except IndexError:
            print(f"\nThe Range {range_id} has a skos:prefLabel without languages: {descriptions}\n\n")
            self.labels = description[0][0].replace("\"", "")

        # skos:notation
        position = data[1].index('skos:notation') + 1
        self.notation = data[1][position][0][0].replace("\"", "")

        # Complete the id
        self.id = data[0]
