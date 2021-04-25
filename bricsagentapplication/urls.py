from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('articles/all', views.get_all_articles, name='get_all_articles'),
    path('articles/some', views.get_some_articles, name='get_some_articles'),
    path('activity', views.get_pub_activity, name='get_pub_activity'),
    path('organizations/top', views.get_top_organizations, name='get_top_organizations'),
    path('keywords/top', views.get_top_keywords, name='get_top_keywords'),
    path('organizations/limit', views.get_limit_organizations, name='get_limit_organizations'),
    path('statistic/period', views.get_statistic_period, name='get_statistic_period'),
    path('organizations/search', views.search_organizations, name='search_organizations'),
    path('redirect', views.redirect_to, name='redirect_to'),
    path('progress', views.filling_progress, name='filling_progress')
]
