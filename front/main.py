import requests
import json

from flask import Flask, render_template,abort,jsonify,request,redirect,url_for
from datetime import datetime

#set FLASK_ENV=development
#set FLASK_APP=main

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])

def welcome():
    return render_template("test.html")


@app.route("/test",methods=["GET","POST"])
def test():
    url="http://127.0.0.1:8000/login"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    user_info={'username':'jose2@email.com',
    'password':'password123'}
    # token_info= requests.post(url,data=user_info,headers=headers).content
    r= requests.post(url,data=user_info,headers=headers)
    token_info=r.json()
    acces_token=token_info['access_token']
    token_type=token_info['token_type']
    return "succesfull"

@app.route("/meals",methods=["GET","POST"])
def get_meals():
    url="http://127.0.0.1:8000/meals"
    headers={'authorization':"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjozLCJleHAiOjE2NTc5OTI1MTl9.qwmGu6AYQGFCBIRHAz0VSimLzU1vFPEnLaie35y5-ks"}
    return requests.get(url,headers=headers).content
