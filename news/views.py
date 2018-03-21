from django.shortcuts import render
from django import template
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.conf import settings

import json
import requests
from bs4 import BeautifulSoup

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def get_news(theme):
    response = requests.get('https://news.yandex.ru/' + theme + '.rss')
    news = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
    news_dict = {}
    i=0
    for site in range(2, len(news.find_all('title'))):
        news_dict[i] = {}
        news_dict[i]['title'] = news.find_all('title')[site].text
        news_dict[i]['url'] = news.find_all('guid')[site-2].text
        i+=1
    return news_dict

def get_kurs(valute):
    response = requests.get('https://api.cryptonator.com/api/ticker/'+ valute + '-rub', timeout=5).json()
    return response['ticker']['price']

def create_list():
    dic = {}
    dic['Технологии'] = get_news('computers')
    dic['Экономика'] = get_news('business')
    dic['Спорт'] = get_news('sport')
    dic['Авто'] = get_news('auto')
    return dic

@cache_page(CACHE_TTL)
def index(request):
    create_list()
    news = {
         'news': create_list(),
         'usd': round(float(get_kurs('usd')), 2),
         'euro': round(float(get_kurs('eur')), 2),
         'bitcoin': round(float(get_kurs('btc'))),
         }
    return render(request,'news/index.html', news )
