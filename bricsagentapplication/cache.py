class Cache:

    def __init__(self):
        self.top_universities = {}
        self.top_keywords = {}
        self.statistic_period = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Cache, cls).__new__(cls)
        return cls.instance

    def cache_unis_top(self, unis, country):
        self.top_universities[country] = []
        for u in unis:
            self.top_universities[country].append(u)

    def cache_keywords_top(self, keywords, country):
        self.top_keywords[country] = []
        for k in keywords:
            self.top_keywords[country].append(k)

    def cache_statistic_period(self, period):
        self.statistic_period['min_date'] = period['min_date']
        self.statistic_period['max_date'] = period['max_date']

    def get_statistic_period(self):
        return self.statistic_period

    def is_statistic_period_empty(self):
        return len(self.statistic_period) == 0

    def is_unis_empty(self, country):
        try:
            return len(self.top_universities[country]) == 0
        except KeyError:
            return True

    def is_keywords_empty(self, country):
        try:
            return len(self.top_keywords[country]) == 0
        except KeyError:
            return True

    def get_unis_top(self, country):
        return self.top_universities[country]

    def get_keywords_top(self, country):
        return self.top_keywords[country]