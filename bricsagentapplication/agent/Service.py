from Project.resources.consts import ALL_COUNTRIES
from .Repo import Repo

from bricsagentapplication.model.models import Keyword, Organization, Author, Publication


class Service:
    def __init__(self):
        self.repo = Repo()

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Service, cls).__new__(cls)
        return cls.instance

    def save_publication_info(self, publication_info):
        if publication_info is not None:
            publication = self.build_publication(publication_info)
            publication = self.repo.save_publication(publication)

            for k in publication_info.keywords:
                if len(k) > 2:
                    keyword = self.build_keyword(k.lower().strip())
                    keyword = self.repo.save_keyword(keyword)
                    if keyword is not None:
                        publication.keywords.add(keyword)

            for u in publication_info.org_authors:
                organization = self.build_org(u)
                if len(organization.name) < 350:
                    organization = self.repo.save_organization(organization)
                    publication.organizations.add(organization)
                    for a in publication_info.org_authors[u]:
                        author = self.build_author(a)
                        author = self.repo.save_author(author)
                        author.organizations.add(organization)
                        publication.authors.add(author)

    def build_publication(self, publication_info):
        publication = Publication()
        publication.name = publication_info.name
        publication.journal_name = publication_info.journal_name
        publication.link = publication_info.link
        publication.link_to_btn = publication_info.link_to_btn
        publication.abstract = publication_info.abstract
        publication.date = publication_info.date
        publication.country = publication_info.country
        return publication

    def build_keyword(self, k):
        keyword = Keyword(name=k)
        return keyword

    def build_org(self, u):
        org = Organization(name=u.strip())
        return org

    def build_author(self, a):
        author = Author(name=a)
        return author

    # ----------------------- organizations

    def get_country_orgs_top(self, country):
        return self.repo.get_country_orgs_top(country)

    def get_all_orgs_top(self):
        return self.repo.get_all_orgs_top()

    def get_limit_organizations(self, country, page):
        orgs = self.repo.get_limit_organizations(country)
        if len(orgs[page*10:]) >= 10:
            return orgs[page*10:page*10+10]
        else:
            return orgs[page*10:]

    def search_orgs_by_name(self, search_text, count_from, count_to, country, page):
        orgs = self.repo.search_orgs_by_name(search_text, count_from, count_to, country)
        if len(orgs[page*10:]) >= 10:
            return orgs[page*10:page*10+10]
        else:
            return orgs[page*10:]

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
            print("Activity for ", country, "...")
            count = self.repo.get_country_activity(country)
            contribution = self.repo.get_coutry_contribution(country)
            activity.append({'country': country, 'count': count, 'contribution':  contribution})
        return activity

    def get_countries_collaborations(self):
        return self.repo.get_countries_collaborations()



