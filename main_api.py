# importing external libraries
from datetime import datetime
import os
import pytz
import requests
import math


# api urls as variables
API_URL = ('http://api.openweathermap.org/data/2.5/weather?q={}&appid={}')
AREA_URL = (
    'http://api.openweathermap.org/data/2.5/box/city?bbox={},{},{},{},{}&appid={}')


# function to get api data by city
def query_api(key, city):
    try:
        print(API_URL.format(city, key))
        data = requests.get(API_URL.format(city, key)).json()
    except Exception as exc:
        print(exc)
        data = None
    return data


# function to get api data by area
def query_api_area(key, lol, lab, lor, lat, z):
    try:
        print(AREA_URL.format(lol, lab, lor, lat, z, key))
        data = requests.get(AREA_URL.format(
            lol, lab, lor, lat, z, key)).json()
    except Exception as exc:
        print(exc)
        data = None
    return data
