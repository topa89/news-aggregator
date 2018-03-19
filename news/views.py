from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django import template
import json


def get_news():
    response = requests.get('https://news.yandex.ru/computers.rss')
    news = BeautifulSoup(response.content.decode('utf-8'), 'html.parser')
    news_dict = {}
    i=0
    for site in range(2, len(news.find_all('title'))):
        news_dict[i] = {}
        news_dict[i]['title'] = news.find_all('title')[site].text
        news_dict[i]['url'] = news.find_all('guid')[site-2].text
        i+=1
    print(news_dict[0]['title'])
    return news_dict

def get_kurs(valute):
    response = requests.get('https://api.cryptonator.com/api/ticker/'+ valute + '-rub', timeout=5).json()
    return response['ticker']['price']

def index(request):
    news = {
         'news': get_news(),
         'usd': round(float(get_kurs('usd')), 2),
         'euro': round(float(get_kurs('eur')), 2),
         'bitcoin': round(float(get_kurs('btc'))),
         }
    return render(request,'news/index.html', news )
