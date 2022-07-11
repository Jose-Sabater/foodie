from typing import List,Optional
from psycopg.rows import dict_row
from fastapi import Body, FastAPI,Response, status,HTTPException, Depends,APIRouter
from .. import schemas,models
from ..database import get_db  
from sqlalchemy.orm import Session
import json

router=APIRouter(
    prefix="/meals",
    tags=['meals']
)


@router.get("/", response_model=List[schemas.Meal])
# @router.get("/",response_model=List[schemas.meal]) #list is from typing to put all meal into a schema
def get_meals(db: Session = Depends(get_db), limit :int = 10, skip: int = 0):
    meals=db.query(models.Meal).limit(limit).offset(skip).all()
    return meals

@router.post("/",status_code=status.HTTP_201_CREATED)
def post_meals(meal:schemas.MealCreate,db: Session = Depends(get_db)):
    food_calories = db.query(models.Calories.cals_pergram).filter(models.Calories.fooditem==meal.meal).first()
    food_alternatives = db.query(models.Calories.fooditem).filter(models.Calories.fooditem.like(f'%{str(meal.meal)}%'))
    if not food_calories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"food {str(meal.meal)} was not found did you mean {[d['fooditem'] for d in food_alternatives]}")
    calories_consumed = meal.quantity * food_calories['cals_pergram']
    meal_dictionary = meal.dict()
    meal_dictionary['calories_consumed'] = calories_consumed
    new_meal=models.Meal(**meal_dictionary)
    print(new_meal)
    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)
    return new_meal