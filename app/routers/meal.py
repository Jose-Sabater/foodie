from typing import List,Optional
from psycopg.rows import dict_row
from fastapi import Body, FastAPI,Response, status,HTTPException, Depends,APIRouter
from sqlalchemy import func
from .. import schemas,models, oath2
from ..database import get_db  
from sqlalchemy.orm import Session
import json

router=APIRouter(
    prefix="/meals",
    tags=['meals']
)


@router.get("/", response_model=List[schemas.Meal])
# @router.get("/",response_model=List[schemas.meal]) #list is from typing to put all meal into a schema
def get_meals(db: Session = Depends(get_db), current_user:int =Depends(oath2.get_current_user), 
                limit :int = 10, skip: int = 0, search: Optional[str]=""):
    meals=db.query(models.Meal).order_by(models.Meal.meal_id).filter(
            models.Meal.meal.contains(search)).limit(limit).offset(skip).all()
    return meals


@router.post("/",status_code=status.HTTP_201_CREATED)
def meal_meals(meal:schemas.MealCreate,db: Session = Depends(get_db),
            current_user:int =Depends (oath2.get_current_user)):
    food_calories = db.query(models.Calories.cals_pergram).filter(models.Calories.fooditem==meal.meal).first()
    food_alternatives = db.query(models.Calories.fooditem).filter(models.Calories.fooditem.like(f'%{str(meal.meal)}%'))
    if not food_calories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"food {str(meal.meal)} was not found did you mean {[d['fooditem'] for d in food_alternatives]}")
    calories_consumed = meal.quantity * food_calories['cals_pergram']
    meal_dictionary = meal.dict()
    meal_dictionary['calories_consumed'] = calories_consumed
    new_meal=models.Meal(user_id=current_user.id,**meal_dictionary)
    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)
    return new_meal


@router.get("/daterange",response_model=List[schemas.Meal])
def get_daterange(date_range : schemas.Daterange, db: Session = Depends(get_db)):
    meal_query = db.query(models.Meal).filter(models.Meal.date > date_range.start_date,
                        models.Meal.date < date_range.end_date ).all()
    if not meal_query:
    # one way to do it:
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'message': f"{id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"no meals between selected dates")
    return  meal_query

@router.get("/usermeals", response_model=List[schemas.Meal])
# @router.get("/",response_model=List[schemas.meal]) #list is from typing to put all meal into a schema
def get_meals(db: Session = Depends(get_db), current_user:int =Depends(oath2.get_current_user)):
    meals=db.query(models.Meal).filter(models.Meal.user_id==current_user.id).all()
    if not meals:
    # one way to do it:
    # response.status_code = status.HTTP_404_NOT_FOUND
    # return {'message': f"{id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"no meals for selected user")
    return meals

@router.get("/{id}",response_model=schemas.Meal) #id is a path parameter
def get_meal(id: int, db: Session = Depends(get_db)):
    #look for first instance, could also do .all
    meal = db.query(models.Meal).filter(models.Meal.meal_id==id).first()   
    if not meal:
        # one way to do it:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"{id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"meal with id {id} was not found")
    return  meal

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meal(id : int, db: Session = Depends(get_db)):
    meal_query=db.query(models.Meal).filter(models.Meal.meal_id == id)
    meal=meal_query.first()
    if meal == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"meal with id {id} does not exist")
    
    # if meal.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                          detail=f"{id} is not authorized to perform action")

    meal_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Meal)  
def update_meal(id:int, updated_meal: schemas.MealCreate,db: Session = Depends(get_db)):

    
    meal_query=db.query(models.Meal).filter(models.Meal.meal_id == id)
    meal=meal_query.first()
    if meal == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"Meal with id {id} does not exist")

    # if meal.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                          detail=f"{id} is not authorized to perform action")

    meal_query.update(updated_meal.dict(),synchronize_session=False)
    db.commit()
    return  meal_query.first()

