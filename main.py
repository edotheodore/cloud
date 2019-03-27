# Theodore Hinanto
# QMUL Cloud Computing ECS781P

# external libraries
from pprint import pprint as pp
from flask import Flask, flash, redirect, render_template, request, url_for, session, abort
from main_api import query_api, query_api_area
from dbcassandra import table_exist, insertData, searchCity
import os
import json
import csv
import cgi

# initialize flask with secret apikey
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
API_KEY = app.config['MY_API_KEY']

# home and login
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                request.form['password'] != 'admin':
            error = 'Invalid credentials'
        else:
            flash('You were successfully logged in')
            return url_for('index')
    return render_template('login.html', error=error)


# index page after login
@app.route('/index', methods=['GET', 'POST'])
def index():
    checktable = table_exist()
    pp(checktable)
    insertData()
    rows = searchCity("def")
    print (rows)
    for weather in rows:
        print ("this is ", weather)
    return render_template(
        'index.html',
        data=rows)


# result page
@app.route('/result', methods=['GET', 'POST'])
def result():
    data = []
    error = None
    select = request.form.get('selector')
    print(select)
    resp = query_api(API_KEY, select)
    # pp(resp)
    if resp:
        data.append(resp)
    if len(data) != 2:
        error = 'Bad Response from Weather API'
    return render_template(
        'result.html',
        data=data,
        error=error)


# list of countries and temperature based from area
@app.route('/tablelist', methods=['POST'])
def tablelist():
    lonleft = request.form.get('lonleft')
    latbottom = request.form.get('latbottom')
    lonright = request.form.get('lonright')
    lattop = request.form.get('lattop')
    zoom = request.form.get('zoom')
    param = [lonleft, latbottom, lonright, lattop, zoom]
    print(param)
    resp = query_api_area(API_KEY, lonleft, latbottom, lonright, lattop, zoom)
    # pp(resp)
    return render_template(
        'tablelist.html',
        data=resp,
        params=param)


# result page based on a certain cityname
@app.route('/result1/<cityname>', methods=['GET', 'POST'])
def result1(cityname):
    data = []
    error = None
    print(cityname)
    select = searchCity(cityname)
    resp = query_api(API_KEY, cityname)
    pp(resp)
    if resp:
        data.append(resp)
    if len(data) != 2:
        error = 'Bad Response from Weather API'
    return render_template(
        'result.html',
        data=data,
        error=error)


if __name__ == '__main__':
    app.run(port=8080, debug=True)
