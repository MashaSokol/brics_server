from django.db import models


class University(models.Model):
    name = models.CharField(max_length=400, null=False, unique=True)


class Author(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    universities = models.ManyToManyField(University)


class Keyword(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)


class Article(models.Model):
    link_to_btn = models.CharField(max_length=300, unique=True)
    link = models.CharField(max_length=300, unique=True)
    journal_name = models.CharField(max_length=1900)
    name = models.CharField(max_length=1500, unique=True)
    abstract = models.CharField(max_length=4000, null=True)
    publication_date = models.DateField(default='0000-1-1')
    country = models.CharField(max_length=50, default='no country')
    authors = models.ManyToManyField(Author)
    universities = models.ManyToManyField(University)
    keywords = models.ManyToManyField(Keyword)


