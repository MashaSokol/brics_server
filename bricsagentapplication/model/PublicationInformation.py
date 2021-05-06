class PublicationInformation:
    def __init__(self):
        self.keywords = []
        self.org_authors = {}
        self.link_to_btn = ''
        self.link = ''
        self.journal_name = ''
        self.name = ''
        self.abstract = ''
        self.date = ''
        self.country = ''

    def to_string(self):
        keyword_string = '\n'
        for keyword in self.keywords:
            keyword_string += '  ' + keyword + '\n'
        org_authors_string = ''
        for u in self.org_authors:
            org_authors_string += '  ' + u + ':\n'
            for a in self.org_authors[u]:
                org_authors_string += '    ' + a + '\n'
        publication_string = 'Link to button: ' + self.link_to_btn + '\n' \
                         + 'Link: ' + self.link + '\n' \
                         + 'Name: ' + self.name + '\n' \
                         + 'Journal name: ' + self.journal_name + '\n' \
                         + 'Annotation: ' + self.abstract + '\n' \
                         + 'Publication date: ' + self.date + '\n' \
                         + 'Country: ' + self.country + '\n' \
                         + 'Keywords: ' + keyword_string + '\n' \
                         + 'Organizations and authors:\n' + org_authors_string
        return publication_string
