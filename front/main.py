import requests
import json
from flask import Flask, render_template,request,redirect,url_for
from .config import settings


#set FLASK_ENV=development
#set FLASK_APP=main


app = Flask(__name__)


@app.route("/",methods=["GET","POST"])
def welcome():
    if request.method == 'POST' and 'uname' in request.form:
        username = request.form.get('uname')
        password = request.form.get('psw')
        LOGIN_URL = settings.back_login
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        user_info={'username': username,'password': password}
        print("sending request")
        response = requests.post(LOGIN_URL, data=user_info, headers=headers)
        token_info = response.json()
        access_token = token_info['access_token']
        token_type=token_info['token_type']
        print("successfully logged in",access_token)
        #add if response succesful or not
        return redirect(url_for('successful',token=access_token))
    return render_template("welcome.html")


@app.route("/successful/<token>",methods=["GET","POST"])
def successful(token):    
    headers={'authorization':"Bearer "+ token}
    login_url= settings.back_meals
    last_meal_url = settings.back_last_meal
    r = requests.get(last_meal_url,headers=headers)
    meal = r.json()
    meal1 = meal[0]
    meal2 = meal[1]
    meal3 = meal[2]
    if request.method == 'POST' and 'meal-token' in request.form:
        print(headers)
        token = request.form.get('meal-token')
        response = requests.get(login_url,headers=headers)
        meals = response.json()
        print(meals)
        return redirect(url_for('get_meals'))
    return render_template("login.html",token=token, meal1=meal1,meal2=meal2, meal3=meal3 )


@app.route("/meals",methods=["GET","POST"])
def get_meals():
    login_url = settings.back_meals
    if request.method == 'POST':
        token = request.form.get('thetoken')
        headers={'authorization':"Bearer "+ token}
        print("headers",headers)
        response = requests.get(login_url,headers=headers)
        meals = response.json()
        print(meals[0]['meal'])
        return render_template('meals.html', meals=meals)
    return render_template('meals.html')


@app.route("/test",methods=["GET","POST"])
def test():
    dict_test = {"key1":10, "k2":'hello'}
    return render_template('test.html',text_lists=dict_test)


