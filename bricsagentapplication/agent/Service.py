from Project.resources.consts import ALL_COUNTRIES
from .Repo import Repo

from bricsagentapplication.model.models import Keyword, Organization, Author, Publication
from ..model.Collaborations import Collaborations


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

    def get_country_organizations_top(self, country):
        return self.repo.get_country_organizations_with_pub_count(country)[:10]

    def get_all_organizations_top(self):
        return self.repo.get_all_organizations_with_pub_count()[:10]

    def get_limit_organizations_with_pub_count(self, country, page):
        orgs = self.repo.get_country_organizations_with_pub_count(country)
        if len(orgs[page*10:]) >= 10:
            return orgs[page*10:page*10+10]
        else:
            return orgs[page*10:]

    def search_orgs_with_pub_count(self, search_text, count_from, count_to, country, page):
        orgs = self.repo.search_orgs_with_pub_count(search_text, count_from, count_to, country)
        if len(orgs[page*10:]) >= 10:
            return orgs[page*10:page*10+10]
        else:
            return orgs[page*10:]

    def get_organization_publications_count(self, organization_id):
        return {'organization_id': organization_id, 'count': self.repo.get_organization_publications_count(organization_id)[0]['count']}
    # ----------------------- keywords

    def get_country_keywords_top(self, country):
        return self.repo.get_country_keywords_with_pub_count(country)[:10]

    def get_all_keywords_top(self):
        return self.repo.get_all_keywords_with_pub_count()[:10]

    # ----------------------- authors

    def get_organization_authors_top(self, organization_id):
        authors = self.repo.get_organization_authors_with_pub_count(organization_id)[:10]
        return {'organization_name': Organization.objects.get(id=organization_id).name, 'authors_top': authors}

    # ----------------------- statistic

    def get_statistic_period(self):
        min_date = self.repo.get_min_pub_date()
        max_date = self.repo.get_max_pub_date()
        return {'min_date': min_date, 'max_date': max_date}

    def get_pub_activity(self):
        publications = self.repo.get_all_publications()
        activity = {c: 0 for c in ALL_COUNTRIES}
        contribution = {c: 0 for c in ALL_COUNTRIES}
        publications_count = 0
        for a in publications:
            orgs = self.repo.get_pub_organizations(a)
            if len(orgs) > 0:
                for c in ALL_COUNTRIES:
                    country_publication_orgs_count = len(self.repo.filter_orgs_by_country(orgs, c))
                    if country_publication_orgs_count > 0:
                        activity[c] += 1
                        contribution[c] += country_publication_orgs_count * 100 / len(orgs)
                publications_count += 1
        for c in contribution:
            contribution[c] = contribution[c] / activity[c]
        result_activity = []
        for country in ALL_COUNTRIES:
            result_activity.append({'country': country, 'count': activity[country], 'contribution':  contribution[country]})
        return result_activity

    def get_countries_collaborations(self):
        all_collaborations = Collaborations()
        # todo убрать 500
        all_publications = self.repo.get_all_publications()[0: 500]
        for a in all_publications:
            print(" ----- ", a.name)
            orgs = []
            for country in ALL_COUNTRIES:
                all_orgs = a.organizations.all()
                orgs.append(len(self.repo.filter_orgs_by_country(all_orgs, country)))
            for i in range(0, len(orgs)):
                if orgs[i]:
                    for j in range(i + 1, len(orgs)):
                        if orgs[j]:
                            all_collaborations.add_collab(ALL_COUNTRIES[i], ALL_COUNTRIES[j], a.keywords.all())
        return all_collaborations.collaborations



