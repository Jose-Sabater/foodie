from ast import Store
import requests
import json
from flask import Flask, render_template,abort,jsonify,request,redirect,url_for,make_response
from datetime import datetime
from flask_jsglue import JSGlue
from selenium import webdriver
import time
#set FLASK_ENV=development
#set FLASK_APP=main


app = Flask(__name__)
@app.route("/",methods=["GET","POST"])
def welcome():
    if request.method == 'POST' and 'uname' in request.form:
        username = request.form.get('uname')
        password = request.form.get('psw')
        login_url="http://127.0.0.1:8000/login"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        user_info={'username':username,
                'password': password}
        response = requests.post(login_url, data=user_info, headers=headers)
        token_info = response.json()
        access_token = token_info['access_token']
        token_type=token_info['token_type']
        print("successfully loged in",access_token)
        return redirect(url_for('successful',token=access_token))
    return render_template("welcome.html")

@app.route("/successful/<token>",methods=["GET","POST"])
def successful(token):
    login_url="http://127.0.0.1:8000/meals"
    if request.method == 'POST' and 'thetoken' in request.form:
        token = request.form.get('thetoken')
        headers={'authorization':"Bearer "+ token}
        print(headers)
        response = requests.get(login_url,headers=headers)
        meals = response.json()
        print(meals)
        return redirect(url_for('get_meals'))
    return render_template("login.html",token=token)


@app.route("/meals",methods=["GET","POST"])
def get_meals():
    login_url="http://127.0.0.1:8000/meals"
    if request.method == 'POST':
        token = request.form.get('thetoken')
        headers={'authorization':"Bearer "+ token}
        print(headers)
        response = requests.get(login_url,headers=headers)
        meals = response.json()
        print(meals)
    return render_template('meals.html')


@app.route("/test",methods=["GET","POST"])
def test():
    start = time.time()
    url="http://127.0.0.1:8000/login"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    user_info={'username':'jose2@email.com',
    'password':'password123'}
    r= requests.post(url,data=user_info,headers=headers)
    token_info=r.json()
    acces_token=token_info['access_token']
    token = acces_token
    end=time.time()
    print(end-start)
    return render_template("test.html", token=token)


@app.route("/retrieval",methods=["GET","POST"])
def retrieval():
    # if request.method = 'POST':
    #     token=request.
    # print("the token is")
    # print(r)
    if request.method == 'POST':

        result = request.form.get('thetoken')

        print(result)
    return render_template("retrieval.html")