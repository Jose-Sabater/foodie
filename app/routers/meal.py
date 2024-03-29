from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, oath2
from ..database import get_db

router = APIRouter(prefix="/meals", tags=["meals"])


@router.get("/", response_model=List[schemas.Meal])
# @router.get("/",response_model=List[schemas.meal]) #list is from typing to
# put all meal into a schema
def get_meals(
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
) -> list:
    meals = (
        db.query(models.Meal)
        .order_by(models.Meal.meal_id)
        .filter(models.Meal.meal.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return meals


@router.post("/", status_code=status.HTTP_201_CREATED)
def meal_meals(
    meal: schemas.MealCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oath2.get_current_user),
) -> dict:
    food_calories = (
        db.query(models.Calories.cals_pergram)
        .filter(models.Calories.fooditem == meal.meal)
        .first()
    )
    food_alternatives = db.query(models.Calories.fooditem).filter(
        models.Calories.fooditem.like(f"%{str(meal.meal)}%")
    )
    if not food_calories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"""food {str(meal.meal)} was not found
                            did you mean
                            {[d['fooditem'] for d in food_alternatives]}""",
        )
    calories_consumed = meal.quantity * food_calories["cals_pergram"]
    meal_dictionary = meal.dict()
    meal_dictionary["calories_consumed"] = calories_consumed
    new_meal = models.Meal(user_id=current_user.id, **meal_dictionary)
    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)
    return new_meal


@router.get("/daterange", response_model=List[schemas.Meal])
def get_daterange(
    date_range: schemas.Daterange, db: Session = Depends(get_db)
) -> dict:
    meal_query = (
        db.query(models.Meal)
        .filter(
            models.Meal.date > date_range.start_date,
            models.Meal.date < date_range.end_date,
        )
        .all()
    )
    if not meal_query:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no meals between selected dates",
        )
    return meal_query


@router.get("/usermeals", response_model=List[schemas.Meal])
def get_meals_ofuser(
    db: Session = Depends(get_db),
    current_user: int = Depends(oath2.get_current_user),
) -> list:
    meals = (
        db.query(models.Meal)
        .filter(models.Meal.user_id == current_user.id)
        .order_by(models.Meal.date.desc())
        .all()
    )
    if not meals:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no meals for selected user",
        )
    return meals


@router.get("/userlastmeal", response_model=List[schemas.Meal])
def get__last_meals(
    db: Session = Depends(get_db),
    current_user: int = Depends(oath2.get_current_user),
) -> list:
    meals = (
        db.query(models.Meal)
        .filter(models.Meal.user_id == current_user.id)
        .order_by(models.Meal.date.desc())
        .limit(3)
        .all()
    )
    if not meals:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no meals for selected user",
        )
    return meals


@router.get("/{id}", response_model=schemas.Meal)  # id is a path parameter
def get_meal(id: int, db: Session = Depends(get_db)) -> dict:
    meal = db.query(models.Meal).filter(models.Meal.meal_id == id).first()
    if not meal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"meal with id {id} was not found",
        )
    return meal


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_meal(id: int, db: Session = Depends(get_db)) -> str:
    meal_query = db.query(models.Meal).filter(models.Meal.meal_id == id)
    meal = meal_query.first()
    if meal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="meal with id {id} does not exist",
        )
    meal_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Meal)
def update_meal(
    id: int, updated_meal: schemas.MealCreate, db: Session = Depends(get_db)
) -> dict:

    meal_query = db.query(models.Meal).filter(models.Meal.meal_id == id)
    meal = meal_query.first()
    if meal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meal with id {id} does not exist",
        )
    meal_query.update(updated_meal.dict(), synchronize_session=False)
    db.commit()
    return meal_query.first()
