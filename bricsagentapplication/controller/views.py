from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from bricsagentapplication.agent.Service import Service
from bricsagentapplication.agent.Agent import Agent

from Project.resources.consts import ALL_COUNTRIES

import threading
import json

from bricsagentapplication.cache.Cache import Cache
from bricsagentapplication.model.models import Publication
from django.core import serializers

agent = Agent()
service = Service()
cache = Cache()


#  -----------------------------------------------------------  parsing
@csrf_exempt
@require_http_methods(["POST"])
def index(request):
    if not request.user.is_superuser:
        request.session['previous_link'] = request.META.get('HTTP_REFERER')
        return HttpResponse(status=401)
    if 0 < agent.get_filling_progress()['progress'] < 100:
        return HttpResponse(status=423)
    threading.Thread(target=agent.fill_db_for_country, args=(json.loads(request.body)['country'],)).start()
    return HttpResponse(status=200)


def redirect_to(request):
    return HttpResponseRedirect(request.session.get('previous_link'))


@csrf_exempt
@require_http_methods(["GET"])
def filling_progress(request):
    return JsonResponse(agent.get_filling_progress(), safe=False)


#  ----------------------------------------------------------- organizations


@csrf_exempt
@require_http_methods(["POST"])
def get_country_top_organizations(request):
    country = json.loads(request.body)['country']
    if cache.is_orgs_empty(country):
        # unis = agent.get_top_unis_names(country)  # с сайта, нужно парсить - долго
        unis = service.get_country_orgs_top(country)  # из БД согласно данным в ней
        cache.cache_countries_orgs_top(unis, country)
    return JsonResponse(cache.get_orgs_top(country), safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def get_all_top_organizations(request):
    return JsonResponse(service.get_all_orgs_top(), safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def get_limit_organizations(request):
    country = json.loads(request.body)['country']
    page = json.loads(request.body)['page'] - 1
    return JsonResponse(service.get_limit_organizations(country, page), safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def search_organizations(request):
    search_text = json.loads(request.body)['search_text']
    page = json.loads(request.body)['page']-1
    country = json.loads(request.body)['country']
    count_from = json.loads(request.body)['count_from']
    count_to = json.loads(request.body)['count_to']
    unis = service.search_orgs_by_name(search_text, count_from, count_to, country, page)
    return JsonResponse(unis, safe=False)

#  ----------------------------------------------------------- keywords


@csrf_exempt
@require_http_methods(["POST"])
def get_country_top_keywords(request):
    country = json.loads(request.body)['country']
    if cache.is_keywords_empty(country):
        kwds = service.get_country_top_keywords_names(country)  # из БД согласно данным в ней
        cache.cache_keywords_top(kwds, country)
    return JsonResponse(cache.get_keywords_top(country), safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def get_all_top_keywords(request):
    return JsonResponse(service.get_all_keywords_top(), safe=False)

#  ----------------------------------------------------------- authors


@csrf_exempt
@require_http_methods(["POST"])
def get_organization_authors_top(request):
    organization_id = json.loads(request.body)['organization_id']
    return JsonResponse(service.get_organization_authors_top(organization_id), safe=False)

#  ----------------------------------------------------------- activity


@csrf_exempt
@require_http_methods(["GET"])
def get_statistic_period(request):
    if cache.is_statistic_period_empty():
        period = service.get_statistic_period()
        cache.cache_statistic_period(period)
    period = cache.get_statistic_period()
    return JsonResponse(period, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def get_pub_activity(request):
    if cache.is_pub_activity_empty():
        activity = service.get_pub_activity()
        cache.cache_pub_activity(activity)
    activity = cache.get_pub_activity()
    return JsonResponse(activity, safe=False)

from json import JSONEncoder

def _default(self, obj):
    return getattr(obj.__class__, "to_json", _default.default)(obj)

_default.default = JSONEncoder().default
JSONEncoder.default = _default

@csrf_exempt
@require_http_methods(["GET"])
def get_countries_collaborations(request):
    if cache.is_countries_collaborations_empty():
        collaborations = service.get_countries_collaborations()
        cache.cache_countries_collaborations(collaborations)
    collaborations = cache.get_countries_collaborations()
    # collaborations = service.get_countries_collaborations()
    return JsonResponse(collaborations, safe=False)

#  ----------------------------------------------------------- articles


@csrf_exempt
@require_http_methods(["POST"])
def get_all_publications(request):
    min = json.loads(request.body)['min']
    max = json.loads(request.body)['max']
    articles = Publication.objects.all()[min:max + 1]
    return JsonResponse(json.loads(serializers.serialize('json', articles)), safe=False)


