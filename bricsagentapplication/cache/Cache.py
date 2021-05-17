class Cache:

    def __init__(self):
        self.countries_organizations_top = {}
        self.all_organizations_top = []
        self.countries_keywords_top = {}
        self.all_keywords_top = []
        self.statistic_period = {}
        self.pub_activity = []
        self.countries_collaborations = []

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Cache, cls).__new__(cls)
        return cls.instance

    # ----------------------- countries orgs

    def cache_countries_orgs_top(self, orgs, country):
        self.countries_organizations_top[country] = []
        for u in orgs:
            self.countries_organizations_top[country].append(u)

    def is_country_orgs_top_empty(self, country):
        try:
            return len(self.countries_organizations_top[country]) == 0
        except KeyError:
            return True

    def get_country_orgs_top(self, country):
        return self.countries_organizations_top[country]

    # ----------------------- all orgs

    def cache_all_orgs_top(self, orgs):
        self.all_organizations_top = []
        for u in orgs:
            self.all_organizations_top.append(u)

    def is_all_orgs_top_empty(self):
        return len(self.all_organizations_top) == 0


    def get_all_orgs_top(self):
        return self.all_organizations_top

    # ----------------------- countries keywords

    def cache_keywords_top(self, keywords, country):
        self.countries_keywords_top[country] = []
        for k in keywords:
            self.countries_keywords_top[country].append(k)

    def is_keywords_empty(self, country):
        try:
            return len(self.countries_keywords_top[country]) == 0
        except KeyError:
            return True

    def get_keywords_top(self, country):
        return self.countries_keywords_top[country]

    # ----------------------- all keywords

    def cache_all_keywords_top(self, orgs):
        self.all_keywords_top = []
        for u in orgs:
            self.all_keywords_top.append(u)

    def is_all_keywords_top_empty(self):
        return len(self.all_keywords_top) == 0


    def get_all_keywords_top(self):
        return self.all_keywords_top

    # ----------------------- statistic

    def cache_statistic_period(self, period):
        self.statistic_period['min_date'] = period['min_date']
        self.statistic_period['max_date'] = period['max_date']

    def is_statistic_period_empty(self):
        return len(self.statistic_period) == 0

    def get_statistic_period(self):
        return self.statistic_period

    # ----------------------- activity

    def cache_pub_activity(self, activity):
        self.pub_activity = []
        for a in activity:
            self.pub_activity.append(({'country': a['country'], 'count': a['count'], 'contribution':  a['contribution']}))

    def is_pub_activity_empty(self):
        return len(self.pub_activity) == 0

    def get_pub_activity(self):
        return self.pub_activity

    # ----------------------- collaborations

    def cache_countries_collaborations(self, countries_collaborations):
        for collab in countries_collaborations:
            self.countries_collaborations.append(collab)
        # self.countries_collaborations = [[0] * len(countries_collaborations) for i in range(len(countries_collaborations))]
        # for i in range(0, len(countries_collaborations)):
        #     for j in range(0, len(countries_collaborations)):
        #         self.countries_collaborations[i][j] = countries_collaborations[i][j]

    def is_countries_collaborations_empty(self):
        return len(self.countries_collaborations) == 0

    def get_countries_collaborations(self):
        return self.countries_collaborations
