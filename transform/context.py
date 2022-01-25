class Context:
    def __init__(self):
        self.context = {
            "@context": dict()
        }

        # By default the context should include the smart data models context
        self.context['@context'].update({'sdmp': 'https://...'})

    def add_context(self, context):
        self.context['@context'].update(context)

    def get_context(self):
        return self.context

    def print_context(self):
        print(self.context)


if __name__ == '__main__':
    a = Context()

    a.print_context()
    a.add_context({'rdf': '<http://www.w3.org/1999/02/22-rdf-syntax-ns#>'})
    a.print_context()
