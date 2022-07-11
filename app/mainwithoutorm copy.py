import psycopg
import time
from psycopg.rows import dict_row
from fastapi import Body, FastAPI,Response, status,HTTPException
from pydantic import BaseModel, PositiveInt
from datetime import date
from . import schemas
app=FastAPI()

# meal=
# class meal(BaseModel):
#     user_id: int
#     meal: str
#     quantity: int
#     # calories_consumed: float

today = date.today()
print(today)

while True:

    try:
        conn = psycopg.connect( host='localhost', dbname='foodie', user='totis', password='Kindle2018',
                                )
        #the information will be received in dict like language (useful for json)
        cursor=conn.cursor(row_factory=dict_row)
        print("Database connection established")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error:", error)
        time.sleep(2)




@app.get("/")
async def root():
    return {"message" : "Hello World"}


@app.get("/meals")
def get_meals():
    cursor.execute("""SELECT * FROM meals """)
    meals=cursor.fetchall()
    return {"data": meals}


@app.post("/meals",status_code=status.HTTP_201_CREATED)
# def create_meals(payLoad: dict=Body(...)):
def create_meals(meal: schemas.Meal):
    print(meal.meal)
    cursor.execute("""SELECT cals_pergram FROM food_calories WHERE fooditem = %s""", (str(meal.meal),))
    calories_per_food = cursor.fetchone()
    if not calories_per_food:
        cursor.execute("""SELECT fooditem FROM food_calories WHERE fooditem like %s""", (f"%{str(meal.meal)}%",))        
        food_alternatives = cursor.fetchall()
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"food {str(meal.meal)} was not found did you mean {[d['fooditem'] for d in food_alternatives]}")
    calories_consumed = meal.quantity * calories_per_food['cals_pergram']
    cursor.execute("""INSERT INTO meals (user_id,meal,quantity,calories_consumed) VALUES (%s, %s, %s, %s) RETURNING *""",
                    (meal.user_id, meal.meal, meal.quantity, calories_consumed))
    new_entry=cursor.fetchone()
    conn.commit()
    return  new_entry


@app.get("/daterange")
def get_daterange(date_range : schemas.Daterange):
    cursor.execute(""" SELECT * FROM meals
                WHERE date > %s AND date <= %s """,
                (date_range.start_date, date_range.end_date)                                           
                )
    meals_in_daterange = cursor.fetchall()
    if not meals_in_daterange:
    # one way to do it:
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'message': f"{id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"no mneals between selected dates")
    return  meals_in_daterange

@app.delete("/meals/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meal(id : int):
    cursor.execute("""DELETE FROM meals WHERE id = %s RETURNING *""", (str(id),))
    deleted_meal=cursor.fetchone()
    if deleted_meal == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"meal with id {id} does not exist")

    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/meals/{id}")  
def update_meal(id:int ,meal: schemas.MealUpdate):

    cursor.execute("""UPDATE meals SET meal = %s, quantity = %s
                    WHERE meal_id=%s RETURNING *""", (meal.meal, meal.quantity,
                    str(id)))   
    updated_meal=cursor.fetchone()
    if updated_meal == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"meal with id {id} does not exist")
    
    conn.commit()
    return {"data" : updated_meal}



#Todo
"""
Be able to query for all meals inside a specific date, Schemas out and models
be able to query for all meals of a specific user
Add user login/tokenization
See all users
See current user_id
"""