from Project.classes.text_functions import similarity
from bricsagentapplication.model.models import Article, Keyword, Author, University

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
        self.saved_unis = [u.name for u in University.objects.all()]
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

    def save_article(self, article):
        try:
            return Article.objects.get(name=article.name)
        except Article.DoesNotExist:
            article.save()
            print('***************** article saved *****************')
            return Article.objects.get(name=article.name)

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

    def save_university(self, university):
        if university.name in self.saved_unis:
            return University.objects.get(name=university.name)
        for uni_name in self.saved_unis:
            if similarity(uni_name, university.name) > 0.8:
                return University.objects.get(name=uni_name)
        university.save()
        self.saved_unis.append(university.name)
        return University.objects.get(name=university.name)
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
        return Article.objects.order_by('publication_date')[0].publication_date

    def get_max_pub_date(self):
        return Article.objects.order_by('-publication_date')[0].publication_date

    def get_country_activity(self, country):
        return len(Article.objects.filter(country__iexact=country))

    def get_coutry_contribution(self, country):
        articles = Article.objects.filter(country__icontains=country)
        if len(articles) < 1:
            return None
        contribution = 0
        articles_count = 0
        for a in articles:
            orgs_count = len(a.universities.all())
            if orgs_count > 0:
                articles_count += 1
                if country.lower() == 'russia':
                    country_article_orgs_count = len(a.universities.all().filter(name__icontains=country))
                else:
                    country_article_orgs_count = len(a.universities.all().filter(name__iendswith=country))
                contribution += country_article_orgs_count*100/orgs_count
        return contribution/articles_count


    # ----------------------- unis

    def search_unis_by_name(self, search_text, count_from, count_to, country):
        query = ""
        if country.lower() != 'russia':
            country = '%' + country
        else:
            country = '%' + country + '%'
        if count_from == 0 and count_to == 0:
            # return University.objects.filter(name__icontains=country).filter(name__icontains=search_text).filter()
            query = "select university_id, u.name, count(university_id) as count " \
                    "from bricsagentapplication_article_universities au, bricsagentapplication_university u " \
                    f"where au.university_id = u.id and name ilike '{country}' and name ilike '%{search_text}%' " \
                    "group by university_id, u.name order by count(university_id) desc"
        else:
            query = "select university_id, name, count from (select university_id, u.name, count(university_id) as count " \
                    "from bricsagentapplication_article_universities au, bricsagentapplication_university u " \
                    f"where au.university_id = u.id and name ilike '{country}' and name ilike '%{search_text}%' " \
                    "group by university_id, u.name order by count(university_id) desc) z " \
                    f"where count>={count_from} and count<={count_to}"
        cursor = connection.cursor()
        cursor.execute(query)
        row = dict_fetch_all(cursor)
        return row

    def get_country_unis_top(self, country):
        if country.lower() != 'russia':
            country = '%' + country
        else:
            country = '%' + country + '%'
        cursor = connection.cursor()
        query = "select university_id, u.name, count(university_id) " \
                "from bricsagentapplication_article_universities au, bricsagentapplication_university u " \
                f"where au.university_id = u.id and name ilike '{country}' " \
                "group by university_id, u.name order by  count(university_id) DESC LIMIT 10"
        cursor.execute(query)
        row = dict_fetch_all(cursor)
        return row

    def get_unis_top(self):
        cursor = connection.cursor()
        query = "select university_id, u.name, count(university_id) " \
                "from bricsagentapplication_article_universities au, bricsagentapplication_university u " \
                f"where au.university_id = u.id " \
                "and (u.name ilike '%china' or u.name ilike '%south africa' or u.name ilike '%brazil' or u.name ilike '%india' or u.name ilike '%russia%' )" \
                "group by university_id, u.name order by  count(university_id) DESC LIMIT 10"
        cursor.execute(query)
        row = dict_fetch_all(cursor)
        return row

    def get_limit_organizations(self, country):
        if country.lower() != 'russia':
            country = '%' + country
        else:
            country = '%' + country + '%'
        cursor = connection.cursor()
        query = "select university_id, u.name, count(university_id) as count " \
                "from bricsagentapplication_article_universities au, bricsagentapplication_university u " \
                f"where au.university_id = u.id and name ilike '{country}' " \
                "group by university_id, u.name order by count(university_id) desc"
        cursor.execute(query)
        row = dict_fetch_all(cursor)
        return row

    # ----------------------- keywords

    def get_country_keywords_top(self, country):
        if country.lower() != 'russia':
            country = '%' + country
        else:
            country = '%' + country + '%'
        cursor = connection.cursor()
        query = f"select k.id, k.name, count(keyword_id) " \
                f"from bricsagentapplication_article_keywords ak, bricsagentapplication_article a, bricsagentapplication_keyword k " \
                f"where ak.article_id=a.id  and a.country ilike '{country}' and ak.keyword_id=k.id " \
                f"group by 1 " \
                f"order by count(keyword_id) DESC, k.name " \
                f"LIMIT 10 ;"
        cursor.execute(query)
        row = dict_fetch_all(cursor)
        return row

    def get_keywords_top(self):
        cursor = connection.cursor()
        query = f"select k.id, k.name, count(keyword_id) " \
                f"from bricsagentapplication_article_keywords ak, bricsagentapplication_article a, bricsagentapplication_keyword k " \
                f"where ak.article_id=a.id and ak.keyword_id=k.id " \
                f"group by 1 " \
                f"order by count(keyword_id) DESC, k.name " \
                f"LIMIT 10 ;"
        cursor.execute(query)
        row = dict_fetch_all(cursor)
        return row

    # ----------------------- authors

    def get_organization_authors_top(self, organization_id):
        cursor = connection.cursor()
        query = f"select auth.id, auth.name, count(aa.author_id) " \
                f"from bricsagentapplication_article_authors aa, " \
                f"bricsagentapplication_article art, " \
                f"bricsagentapplication_author auth, " \
                f"bricsagentapplication_author_universities au " \
                f"where aa.article_id=art.id and aa.author_id=auth.id and au.author_id=auth.id and au.university_id = {organization_id} " \
                f"group by 1, 2 " \
                f"order by count(aa.author_id) DESC, auth.name " \
                f"LIMIT 10;"
        cursor.execute(query)
        row = dict_fetch_all(cursor)
        answer = {'organization_name': University.objects.get(id=organization_id).name, 'authors_top': row}
        return answer




