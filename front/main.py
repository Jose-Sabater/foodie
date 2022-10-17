from datetime import datetime
import requests
from flask import Flask, render_template, request, redirect, url_for, session
import json
from .config import settings


# set FLASK_ENV=development
# set FLASK_APP=main


app = Flask(__name__)
app.secret_key = settings.flask_secret_key


@app.route("/", methods=["GET", "POST"])
def welcome():
    LOGIN_URL = settings.back_login
    REGISTER_URL = settings.register_url
    if request.method == "POST" and "uname" in request.form:
        username = request.form.get("uname")
        password = request.form.get("psw")
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        user_info = {"username": username, "password": password}
        print("sending request")
        response = requests.post(LOGIN_URL, data=user_info, headers=headers)
        print(response.status_code)
        token_info = response.json()
        access_token = token_info["access_token"]
        # token_type = token_info["token_type"]
        print("successfully logged in", access_token)
        session["token"] = access_token
        return redirect(url_for("successful", token=access_token))

    elif request.method == "POST" and "email" in request.form:
        username = request.form.get("email")
        password = request.form.get("psw")
        # headers = {"Content-Type": "application/x-www-form-urlencoded"}
        user_info = {"email": username, "password": password}
        print("Trying to register user....")
        print(user_info["email"])
        response = requests.post(REGISTER_URL, data=json.dumps(user_info))
        print(response.text)
        # Now log in
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        user_info = {"username": username, "password": password}
        print(f"login in as {username}")
        response = requests.post(LOGIN_URL, data=user_info, headers=headers)
        print(response.status_code)
        token_info = response.json()
        access_token = token_info["access_token"]
        # token_type = token_info["token_type"]
        print("successfully logged in", access_token)
        session["token"] = access_token
        return redirect(url_for("successful", token=access_token))
    return render_template("welcome.html")


@app.route("/successful/<token>", methods=["GET", "POST"])
def successful(token):
    headers = {"authorization": "Bearer " + token}
    login_url = settings.back_meals
    last_meal_url = settings.back_last_meal
    r = requests.get(last_meal_url, headers=headers)
    print(r.text)
    meal = r.json()
    print(f"the meal is {meal}")
    if meal[1] == "no meals for selected user":
        print("redirect to no_meals_yet")
        return render_template("empty_meals.html", token=token)
    meal1 = meal[0]
    meal2 = meal[1]
    meal3 = meal[2]
    if request.method == "POST" and "meal-token" in request.form:
        print(headers)
        token = request.form.get("meal-token")
        response = requests.get(login_url, headers=headers)
        meals = response.json()
        print(meals)
        return redirect(url_for("get_meals"))
    return render_template(
        "login.html", token=token, meal1=meal1, meal2=meal2, meal3=meal3
    )


@app.route("/meals", methods=["GET", "POST"])
def get_meals():
    token = session.get("token", None)
    print("the token is", token)
    login_url = settings.back_meals
    # token = request.form.get('thetoken')
    headers = {"authorization": "Bearer " + token}
    print("headers", headers)
    response = requests.get(login_url, headers=headers)
    meals = response.json()
    for meal in meals:
        # mydate = meal['date'][0:10]
        meal["meal"] = meal["meal"].replace(" ", "-")
        mydate = datetime.fromisoformat(meal["date"])
        mydate = mydate.strftime("%A %d %b %Y")
        meal["date"] = mydate
        imgpath = f"/static/images/{meal['meal']}.jpg"
        meal["imgpath"] = imgpath
    print(meals)
    return render_template("meals.html", meals=meals)


@app.route("/test", methods=["GET", "POST"])
def test():
    dict_test = {"key1": 10, "k2": "hello"}
    return render_template("test.html", text_lists=dict_test)


@app.route("/random-meal", methods=["GET", "POST"])
def random_meal():
    login_url = "http://www.themealdb.com/api/json/v1/1/random.php"
    response = requests.get(login_url)
    meals = response.json()
    random_meal = meals["meals"][0]
    my_meal = dict()
    my_meal["title"] = random_meal["strMeal"]
    my_meal["category"] = random_meal["strCategory"]
    my_meal["area"] = random_meal["strArea"]
    my_meal["instructions"] = random_meal["strInstructions"]
    my_meal["imgpath"] = random_meal["strMealThumb"]
    my_meal["youtube"] = random_meal["strYoutube"]
    return render_template("random-meal.html", my_meal=my_meal)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
