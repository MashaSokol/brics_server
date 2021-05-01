class ArticleInformation:
    def __init__(self):
        self.keywords = []
        self.uni_authors = {}
        self.link_to_btn = ''
        self.link = ''
        self.journal_name = ''
        self.name = ''
        self.abstract = ''
        self.publication_date = ''
        self.country = ''

    def to_string(self):
        keyword_string = '\n'
        for keyword in self.keywords:
            keyword_string += '  ' + keyword + '\n'
        uni_authors_string = ''
        for u in self.uni_authors:
            uni_authors_string += '  ' + u + ':\n'
            for a in self.uni_authors[u]:
                uni_authors_string += '    ' + a + '\n'
        article_string = 'Link to button: ' + self.link_to_btn + '\n' \
                         + 'Link: ' + self.link + '\n' \
                         + 'Name: ' + self.name + '\n' \
                         + 'Jpurnal name: ' + self.journal_name + '\n' \
                         + 'Annotation: ' + self.abstract + '\n' \
                         + 'Publication date: ' + self.publication_date + '\n' \
                         + 'Country: ' + self.country + '\n' \
                         + 'Keywords: ' + keyword_string + '\n' \
                         + 'Universities and authors:\n' + uni_authors_string
        return article_string
