from Project.resources.consts import ALL_COUNTRIES
from .Repo import Repo

from bricsagentapplication.model.models import Keyword, University, Author, Article


class Service:
    def __init__(self):
        self.repo = Repo()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Service, cls).__new__(cls)
        return cls.instance

    def save_article_info(self, article_info):
        if article_info is not None:
            article = self.build_article(article_info)
            article = self.repo.save_article(article)

            for k in article_info.keywords:
                if len(k) > 2:
                    keyword = self.build_keyword(k.lower().strip())
                    keyword = self.repo.save_keyword(keyword)
                    if keyword is not None:
                        article.keywords.add(keyword)

            for u in article_info.uni_authors:
                university = self.build_uni(u)
                if len(university.name) < 350:
                    university = self.repo.save_university(university)
                    article.universities.add(university)
                    for a in article_info.uni_authors[u]:
                        author = self.build_author(a)
                        author = self.repo.save_author(author)
                        author.universities.add(university)
                        article.authors.add(author)

    def build_article(self, article_info):
        article = Article()
        article.name = article_info.name
        article.journal_name = article_info.journal_name
        article.link = article_info.link
        article.link_to_btn = article_info.link_to_btn
        article.abstract = article_info.abstract
        article.publication_date = article_info.publication_date
        article.country = article_info.country
        return article

    def build_keyword(self, k):
        keyword = Keyword(name=k)
        return keyword

    def build_uni(self, u):
        uni = University(name=u.strip())
        return uni

    def build_author(self, a):
        author = Author(name=a)
        return author

    # ----------------------- organizations

    def get_country_unis_top(self, country):
        return self.repo.get_country_unis_top(country)

    def get_all_unis_top(self):
        return self.repo.get_unis_top()

    def get_limit_organizations(self, country, page):
        unis = self.repo.get_limit_organizations(country)
        if len(unis[page*10:]) >= 10:
            return unis[page*10:page*10+10]
        else:
            return unis[page*10:]

    def search_unis_by_name(self, search_text, count_from, count_to, country, page):
        unis = self.repo.search_unis_by_name(search_text, count_from, count_to,  country)
        if len(unis[page*10:]) >= 10:
            return unis[page*10:page*10+10]
        else:
            return unis[page*10:]

    # ----------------------- keywords

    def get_country_top_keywords_names(self, country):
        return self.repo.get_country_keywords_top(country)

    def get_all_keywords_top(self):
        return self.repo.get_keywords_top()

    # ----------------------- authors

    def get_organization_authors_top(self, organization_id):
        return self.repo.get_organization_authors_top(organization_id)

    # ----------------------- statistic

    def get_statistic_period(self):
        min_date = self.repo.get_min_pub_date()
        max_date = self.repo.get_max_pub_date()
        return {'min_date': min_date, 'max_date': max_date}

    def get_pub_activity(self):
        activity = []
        for country in ALL_COUNTRIES:
            count = self.repo.get_country_activity(country)
            contribution = self.repo.get_coutry_contribution(country)
            activity.append({'country': country, 'count': count, 'contribution':  contribution})
        return activity



