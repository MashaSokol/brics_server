from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import PermissionDenied
from django.db import connection

from .Service import Service
from .agent import Agent

from project.resources.consts import COUNTRY, ALL_COUNTRIES

import threading
import json

from .models import Article, University
from django.core import serializers

agent = Agent()
service = Service()

link=""


@csrf_exempt
# @require_http_methods(["GET"])
# @login_required()
# @superuser_only()
def index(request):
    if not request.user.is_superuser:
        # print("http://localhost:8000/accounts/login/?next=" + request.META.get('HTTP_REFERER'))
        # http://localhost:8000/accounts/login/?next=http%3A%2F%2Flocalhost%3A3000%2Fadmin%2F
        print("NOT A SUPER USER, ", request.META.get('HTTP_REFERER'))
        agent.test_link = request.META.get('HTTP_REFERER')
        return HttpResponseRedirect('http://localhost:8000/accounts/login/') # + request.META.get('HTTP_REFERER'))

    # threading.Thread(target=agent.fill_db_for_country, args=(COUNTRY,)).start()

    return HttpResponse("hello")
    # return response
    # return redirect(request.path)


def redirect_to(request):
    return HttpResponseRedirect("http://localhost:3000/admin")

@csrf_exempt
@require_http_methods(["POST"])
def get_all_articles(request):
    min = json.loads(request.body)['min']
    max = json.loads(request.body)['max']
    articles = Article.objects.all()[min:max+1]
    return JsonResponse(json.loads(serializers.serialize('json', articles)), safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def get_statistic_period(request):
    period = service.get_statistic_period()
    return JsonResponse(period, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def search_organizations(request):
    search_text = json.loads(request.body)['search_text']
    page = json.loads(request.body)['page']-1
    country = json.loads(request.body)['country']
    count_from = json.loads(request.body)['count_from']
    count_to = json.loads(request.body)['count_to']
    unis = service.search_unis_by_name(search_text, count_from, count_to, country, page)
    return JsonResponse(unis, safe=False)

@csrf_exempt
@require_http_methods(["GET"])
def get_some_articles(request):
    # min = json.loads(request.body)['min']
    # max = json.loads(request.body)['max']
    articles = Article.objects.all()[1:2+1]
    return JsonResponse(json.loads(serializers.serialize('json', articles)), safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def get_pub_activity(request):
    all = []
    activity = {}
    for country in ALL_COUNTRIES:
        count = len(Article.objects.filter(country=country))
        print(count)
        activity[country] = count
        all.append({'country': country, 'count': count})
    print(activity)
    return JsonResponse(all, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def get_top_organizations(request):
    country = json.loads(request.body)['country']
    return JsonResponse(agent.country_unis_top(country), safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def get_top_keywords(request):
    country = json.loads(request.body)['country']
    return JsonResponse(agent.country_keywords_top(country), safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def get_limit_organizations(request):
    country = json.loads(request.body)['country']
    page = json.loads(request.body)['page'] - 1
    return JsonResponse(agent.get_limit_organizations(country, page), safe=False)
