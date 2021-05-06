from django.db import models

class Collaboration():

    def add_keywords(self, keywords):
        for k in keywords:
            if k.name not in self.keywords:
                self.keywords[k.name] = 0
            self.keywords[k.name] += 1

    def __init__(self, first_country, second_country, keywords):
        self.first_country = first_country
        self.second_country = second_country
        self.count = 1
        self.keywords = {}
        self.add_keywords(keywords)

    def to_json(self):
        return {
            'first_country': self.first_country,
            'second_country': self.second_country,
            'count': self.count,
            'keywords': self.keywords_to_json(self.keywords)
        }

    def keywords_to_json(self, keywords):
        return [{'keyword': k, 'count': keywords[k]} for k in keywords]


class Collaborations:

    def __init__(self):
        self.collaborations = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Collaborations, cls).__new__(cls)
        return cls.instance

    def add_collab(self, first_country, second_country, keywords):
        for collab in self.collaborations:
            if collab.first_country == first_country and collab.second_country == second_country:
                collab.count += 1
                collab.add_keywords(keywords)
                return
        new_collab = Collaboration(first_country, second_country, keywords)
        self.collaborations.append(new_collab)






