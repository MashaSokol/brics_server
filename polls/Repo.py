from .models import Article, Keyword, Author, University
import difflib
from django.db import connection, IntegrityError


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

    def dictfetchall(self, cursor):
        "Returns all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Repo, cls).__new__(cls)
        return cls.instance

    # для поиска Publisher.objects.filter(name__contains="press")  icontains
    # todo должно быть не тут
    def delete_not_alphas(self, str):
        new_str = ""
        for s in str:
            if not s.isalpha():
                new_str += s
        return new_str

    def get_min_pub_date(self):
        return Article.objects.order_by('publication_date')[0].publication_date

    def get_max_pub_date(self):
        return Article.objects.order_by('-publication_date')[0].publication_date

    def search_unis_by_name(self, search_text, count_from, count_to, country):
        query = ""
        if count_from == 0 and count_to == 0:
            # return University.objects.filter(name__icontains=country).filter(name__icontains=search_text).filter()
            query = "select university_id, u.name, count(university_id) as count " \
                    "from polls_article_universities au, polls_university u " \
                    f"where au.university_id = u.id and name ilike '%{country}%' and name ilike '%{search_text}%' " \
                    "group by university_id, u.name order by count(university_id) desc"
        else:
            query = "select university_id, name, count from (select university_id, u.name, count(university_id) as count " \
                    "from polls_article_universities au, polls_university u " \
                    f"where au.university_id = u.id and name ilike '%{country}%' and name ilike '%{search_text}%' " \
                    "group by university_id, u.name order by count(university_id) desc) z " \
                    f"where count>={count_from} and count<={count_to}"
        cursor = connection.cursor()
        cursor.execute(query)
        row = self.dictfetchall(cursor)
        return row

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

    # todo переместить в другое место
    def similarity(self, s1, s2):
        normalized1 = self.delete_not_alphas(s1.lower())
        normalized2 = self.delete_not_alphas(s2.lower())
        matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
        return matcher.ratio()

    def save_university(self, university):
        if university.name in self.saved_unis:
            return University.objects.get(name=university.name)
        for uni_name in self.saved_unis:
            if self.similarity(uni_name, university.name) > 0.8:
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

    def get_country_unis_top(self, country):
        cursor = connection.cursor()
        query = "select university_id, u.name, count(university_id) " \
                "from polls_article_universities au, polls_university u " \
                f"where au.university_id = u.id and name ilike '%{country}%' " \
                "group by university_id, u.name order by  count(university_id) DESC LIMIT 10"
        cursor.execute(query)
        row = self.dictfetchall(cursor)
        return row

    def get_country_keywords_top(self, country):
        cursor = connection.cursor()
        query = f"select k.id, k.name, count(keyword_id) " \
                f"from polls_article_keywords ak, polls_article a, polls_keyword k " \
                f"where ak.article_id=a.id  and a.country ilike '%{country}%' and ak.keyword_id=k.id " \
                f"group by 1 " \
                f"order by count(keyword_id) DESC, k.name " \
                f"LIMIT 10 ;"
        cursor.execute(query)
        row = self.dictfetchall(cursor)
        return row

    def get_limit_organizations(self, country):
        cursor = connection.cursor()
        query = "select university_id, u.name, count(university_id) as count " \
                    "from polls_article_universities au, polls_university u " \
                    f"where au.university_id = u.id and name ilike '%{country}%' " \
                    "group by university_id, u.name order by count(university_id) desc"
        cursor.execute(query)
        row = self.dictfetchall(cursor)
        return row
