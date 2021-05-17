from django.urls import path

from bricsagentapplication.controller import views

urlpatterns = [
    path('start', views.start, name='start'),

    path('articles/all', views.get_all_publications, name='get_all_articles'),
    path('activity', views.get_pub_activity, name='get_pub_activity'),

    path('country/organizations/top', views.get_country_organizations_top, name='get_top_organizations'),
    path('country/keywords/top', views.get_country_keywords_top, name='get_top_keywords'),
    path('organizations/all/top', views.get_all_organizations_top, name='get_all_top_organizations'),
    path('keywords/all/top', views.get_all_keywords_top, name='get_all_top_keywords'),

    path('organizations/limit', views.get_limit_organizations, name='get_limit_organizations'),
    path('organization/authors/top', views.get_organization_authors_top, name='get_organization_authors_top'),
    path('organization/publications/count', views.get_organization_publications_count, name='get_organization_publications_count'),

    path('statistic/period', views.get_statistic_period, name='get_statistic_period'),
    path('organizations/search', views.search_organizations, name='search_organizations'),
    path('redirect', views.redirect_to, name='redirect_to'),
    path('progress', views.filling_progress, name='filling_progress'),

    path('countries/collaborations', views.get_countries_collaborations, name='get_countries_collaborations')
]
