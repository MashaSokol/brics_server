from Project.classes.text_functions import similarity
from Project.resources.consts import ALL_COUNTRIES
from bricsagentapplication.model.Collaborations import Collaborations
from bricsagentapplication.model.Collaborations import Collaboration
from bricsagentapplication.model.models import Publication, Keyword, Author, Organization

from django.db import connection


def dict_fetch_all(cursor):
    """Returns all rows from a cursor as a dict"""
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


class Repo:

    def __init__(self):
        self.saved_orgs = [u.name for u in Organization.objects.all()]
        # self.saved_unis = {}
        # unis_from_db = University.objects.all()
        # for u in unis_from_db:
        #     u.name = self.delete_not_alphas(u.name)
        #     if u.name[0:30] not in self.saved_unis:
        #         self.saved_unis[u.name[0:30]] = []
        #     self.saved_unis[u.name[0:30]].append(u)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Repo, cls).__new__(cls)
        return cls.instance

    # для поиска Publisher.objects.filter(name__contains="press")  icontains

    # ----------------------- saving

    def save_publication(self, publication):
        try:
            return Publication.objects.get(name=publication.name)
        except Publication.DoesNotExist:
            publication.save()
            print('***************** article saved *****************')
            return Publication.objects.get(name=publication.name)

    def save_keyword(self, keyword):
        try:
            return Keyword.objects.get(name=keyword.name)
        except Keyword.DoesNotExist:
            if len(keyword.name) < 255:
                keyword.save()
                return Keyword.objects.get(name=keyword.name)

    def save_author(self, author):
        try:
            return Author.objects.get(name=author.name)
        except Author.DoesNotExist:
            author.save()
            return Author.objects.get(name=author.name)

    def save_organization(self, organization):
        if organization.name in self.saved_orgs:
            return Organization.objects.get(name=organization.name)
        for org_name in self.saved_orgs:
            if similarity(org_name, organization.name) > 0.8:
                return Organization.objects.get(name=org_name)
        organization.save()
        self.saved_orgs.append(organization.name)
        return Organization.objects.get(name=organization.name)
        # try:
        #     return University.objects.get(name=university.name)
        # except University.DoesNotExist:
        #     name = self.delete_not_alphas(university.name)
        #     if name[0:30] in self.saved_unis:
        #         for saved_uni in self.saved_unis[name[0:30]]:
        #             s = self.similarity(name, saved_uni.name)
        #             if s > 0.8:
        #                 return University.objects.get(id=saved_uni.id)
        #     university.save()
        #     university.name = name
        #     self.saved_unis[university.name[0:30]].append(university)
        #     return University.objects.get(id=university.id)

    # ----------------------- statistic period

    def get_min_pub_date(self):
        return Publication.objects.order_by('date')[0].date

    def get_max_pub_date(self):
        return Publication.objects.order_by('-date')[0].date

    def get_all_publications(self):
        return Publication.objects.all()

    def get_pub_organizations(self, publication):
        return publication.organizations.all()

    def get_organization_publications_count(self, organization_id):

        query = f"select count(organization_id) " \
                f"from bricsagentapplication_publication_organizations " \
                f"where organization_id={organization_id}"

        cursor = connection.cursor()
        cursor.execute(query)
        row = dict_fetch_all(cursor)
        print(";;;;;;;;;;;;;;;;;;;;;;;;", row)
        return row

    def filter_orgs_by_country(self, orgs, country):
        return orgs.filter(name__icontains=country) if country.lower() == 'russia' else orgs.filter(name__iendswith=country)
    # # todo создать класс countryActivity
    # def get_countries_activity(self):
    #     publications = Publication.objects.all()
    #
    #     activity = {c: 0 for c in ALL_COUNTRIES}
    #     contribution = {c: 0 for c in ALL_COUNTRIES}
    #     publications_count = 0
    #
    #     for a in publications:
    #         orgs = a.organizations.all()
    #         if len(orgs) > 0:
    #             for c in ALL_COUNTRIES:
    #                 country_publication_orgs_count = len(orgs.filter(name__icontains=c)) if c.lower() == 'russia' else len(orgs.filter(name__iendswith=c))
    #                 if country_publication_orgs_count > 0:
    #                     activity[c] += 1
    #                     contribution[c] += country_publication_orgs_count * 100 / len(orgs)
    #             publications_count += 1
    #     for c in contribution:
    #         contribution[c] = contribution[c] / activity[c]
    # #     return activity, contribution
    #
    # def get_coutry_contribution(self, country):
    #     # articles = Article.objects.filter(country__icontains=country)
    #     publications = Publication.objects.all()
    #     contribution = 0
    #     publications_count = 0
    #     for a in publications:
    #         orgs = a.organizations.all()
    #         if len(orgs) > 0:
    #             country_publication_orgs_count = len(orgs.filter(name__icontains=country)) if country.lower() == 'russia' else len(orgs.filter(name__iendswith=country))
    #             if country_publication_orgs_count > 0:
    #                 publications_count += 1
    #                 contribution += country_publication_orgs_count * 100 / len(orgs)
    #     return contribution / publications_count

    # def get_countries_collaborations(self):
    #     all_collaborations = Collaborations()
    #
    #     # todo убрать 500
    #     all_publications = Publication.objects.all()[0:500]
    #     for a in all_publications:
    #         print(" ----- ", a.name)
    #         orgs = []
    #         for country in ALL_COUNTRIES:
    #             all_orgs = a.organizations.all()
    #             orgs.append(len(all_orgs.filter(name__icontains=country)) > 0) if country.lower() == 'russia' else orgs.append(len(all_orgs.filter(name__iendswith=country)) > 0)
    #         for i in range(0, len(orgs)):
    #             if orgs[i]:
    #                 for j in range(i + 1, len(orgs)):
    #                     if orgs[j]:
    #                         all_collaborations.add_collab(ALL_COUNTRIES[i], ALL_COUNTRIES[j], a.keywords.all())
    #     return all_collaborations.collaborations



    # ----------------------- unis

    def search_orgs_with_pub_count(self, search_text, count_from, count_to, country):
        if country.lower() != 'russia':
            country = '%' + country
        else:
            country = '%' + country + '%'
        if count_from == 0 and count_to == 0:
            query = "select organization_id, u.name, count(organization_id) as count " \
                    "from bricsagentapplication_publication_organizations au, bricsagentapplication_organization u " \
                    f"where au.organization_id = u.id and name ilike '{country}' and name ilike '%{search_text}%' " \
                    "group by organization_id, u.name order by count(organization_id) desc"
        else:
            query = "select organization_id, name, count from (select organization_id, u.name, count(organization_id) as count " \
                    "from bricsagentapplication_publication_organizations au, bricsagentapplication_organization u " \
                    f"where au.organization_id = u.id and name ilike '{country}' and name ilike '%{search_text}%' " \
                    "group by organization_id, u.name order by count(organization_id) desc) z " \
                    f"where count>={count_from} and count<={count_to}"
        cursor = connection.cursor()
        cursor.execute(query)
        row = dict_fetch_all(cursor)
        return row


    # def get_country_orgs_top(self, country):
    #     if country.lower() != 'russia':
    #         country = '%' + country
    #     else:
    #         country = '%' + country + '%'
    #     cursor = connection.cursor()
    #     query = "select organization_id, u.name, count(organization_id) " \
    #             "from bricsagentapplication_publication_organizations au, bricsagentapplication_organization u " \
    #             f"where au.organization_id = u.id and name ilike '{country}' " \
    #             "group by organization_id, u.name order by  count(organization_id) DESC LIMIT 10"
    #     cursor.execute(query)
    #     row = dict_fetch_all(cursor)
    #     return row

    def get_all_organizations_with_pub_count(self):
        cursor = connection.cursor()
        query = "select organization_id, u.name, count(organization_id) " \
                "from bricsagentapplication_publication_organizations au, bricsagentapplication_organization u " \
                f"where au.organization_id = u.id " \
                "and (u.name ilike '%china' or u.name ilike '%south africa' or u.name ilike '%brazil' or u.name ilike '%india' or u.name ilike '%russia%' )" \
                "group by organization_id, u.name order by  count(organization_id) DESC"
        cursor.execute(query)
        row = dict_fetch_all(cursor)
        return row

    # def get_all_orgs_top(self):
    #     cursor = connection.cursor()
    #     query = "select organization_id, u.name, count(organization_id) " \
    #             "from bricsagentapplication_publication_organizations au, bricsagentapplication_organization u " \
    #             f"where au.organization_id = u.id " \
    #             "and (u.name ilike '%china' or u.name ilike '%south africa' or u.name ilike '%brazil' or u.name ilike '%india' or u.name ilike '%russia%' )" \
    #             "group by organization_id, u.name order by  count(organization_id) DESC LIMIT 10"
    #     cursor.execute(query)
    #     row = dict_fetch_all(cursor)
    #     return row

    def get_country_organizations_with_pub_count(self, country):
        if country.lower() != 'russia':
            country = '%' + country
        else:
            country = '%' + country + '%'
        cursor = connection.cursor()
        query = "select organization_id, u.name, count(organization_id) as count " \
                "from bricsagentapplication_publication_organizations au, bricsagentapplication_organization u " \
                f"where au.organization_id = u.id and name ilike '{country}' " \
                "group by organization_id, u.name order by count(organization_id) desc"
        cursor.execute(query)
        row = dict_fetch_all(cursor)
        return row


    # ----------------------- keywords

    def get_country_keywords_with_pub_count(self, country):
        if country.lower() != 'russia':
            country = '%' + country
        else:
            country = '%' + country + '%'
        cursor = connection.cursor()
        query = f"select k.id, k.name, count(keyword_id) " \
                f"from bricsagentapplication_publication_keywords ak, bricsagentapplication_publication a, bricsagentapplication_keyword k " \
                f"where ak.publication_id=a.id  and a.country ilike '{country}' and ak.keyword_id=k.id " \
                f"group by 1 " \
                f"order by count(keyword_id) DESC, k.name "
        cursor.execute(query)
        row = dict_fetch_all(cursor)
        return row
    # def get_country_keywords_top(self, country):
    #     if country.lower() != 'russia':
    #         country = '%' + country
    #     else:
    #         country = '%' + country + '%'
    #     cursor = connection.cursor()
    #     query = f"select k.id, k.name, count(keyword_id) " \
    #             f"from bricsagentapplication_publication_keywords ak, bricsagentapplication_publication a, bricsagentapplication_keyword k " \
    #             f"where ak.publication_id=a.id  and a.country ilike '{country}' and ak.keyword_id=k.id " \
    #             f"group by 1 " \
    #             f"order by count(keyword_id) DESC, k.name " \
    #             f"LIMIT 10 ;"
    #     cursor.execute(query)
    #     row = dict_fetch_all(cursor)
    #     return row

    def get_all_keywords_with_pub_count(self):
        cursor = connection.cursor()
        query = f"select k.id, k.name, count(keyword_id) " \
                f"from bricsagentapplication_publication_keywords ak, bricsagentapplication_publication a, bricsagentapplication_keyword k " \
                f"where ak.publication_id=a.id and ak.keyword_id=k.id " \
                f"group by 1 " \
                f"order by count(keyword_id) DESC, k.name " \
                f"LIMIT 10 ;"
        cursor.execute(query)
        row = dict_fetch_all(cursor)
        return row
    # def get_all_keywords_top(self):
    #     cursor = connection.cursor()
    #     query = f"select k.id, k.name, count(keyword_id) " \
    #             f"from bricsagentapplication_publication_keywords ak, bricsagentapplication_publication a, bricsagentapplication_keyword k " \
    #             f"where ak.publication_id=a.id and ak.keyword_id=k.id " \
    #             f"group by 1 " \
    #             f"order by count(keyword_id) DESC, k.name " \
    #             f"LIMIT 10 ;"
    #     cursor.execute(query)
    #     row = dict_fetch_all(cursor)
    #     return row

    # ----------------------- authors
    def get_organization_authors_with_pub_count(self, organization_id):
        cursor = connection.cursor()
        query = f"select auth.id, auth.name, count(aa.author_id) " \
                f"from bricsagentapplication_publication_authors aa, " \
                f"bricsagentapplication_publication art, " \
                f"bricsagentapplication_author auth, " \
                f"bricsagentapplication_author_organizations au " \
                f"where aa.publication_id=art.id and aa.author_id=auth.id and au.author_id=auth.id and au.organization_id = {organization_id} " \
                f"group by 1, 2 " \
                f"order by count(aa.author_id) DESC, auth.name " \
                f"LIMIT 10;"
        cursor.execute(query)
        row = dict_fetch_all(cursor)
        return row
    # def get_organization_authors_top(self, organization_id):
    #     cursor = connection.cursor()
    #     query = f"select auth.id, auth.name, count(aa.author_id) " \
    #             f"from bricsagentapplication_publication_authors aa, " \
    #             f"bricsagentapplication_publication art, " \
    #             f"bricsagentapplication_author auth, " \
    #             f"bricsagentapplication_author_organizations au " \
    #             f"where aa.publication_id=art.id and aa.author_id=auth.id and au.author_id=auth.id and au.organization_id = {organization_id} " \
    #             f"group by 1, 2 " \
    #             f"order by count(aa.author_id) DESC, auth.name " \
    #             f"LIMIT 10;"
    #     cursor.execute(query)
    #     row = dict_fetch_all(cursor)
    #     return row
