from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=400, null=False, unique=True)


class Author(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)
    organizations = models.ManyToManyField(Organization)


class Keyword(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True)


class Publication(models.Model):
    link_to_btn = models.CharField(max_length=300, unique=True)
    link = models.CharField(max_length=300, unique=True)
    journal_name = models.CharField(max_length=1900)
    name = models.CharField(max_length=1500, unique=True)
    abstract = models.CharField(max_length=4000, null=True)
    date = models.DateField(default='0000-1-1')
    country = models.CharField(max_length=50, default='no country')
    authors = models.ManyToManyField(Author)
    organizations = models.ManyToManyField(Organization)
    keywords = models.ManyToManyField(Keyword)


