from typing import Optional
from pydantic import BaseModel, PositiveInt, EmailStr, conint 
from datetime import datetime, date


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    age: str


class MealBase(BaseModel):
    user_id: int
    meal: str
    quantity: int
    class Config:
        orm_model=True

class Meal(MealBase):
    calories_consumed: float

    class Config:
        orm_mode=True

class MealCreate(MealBase):
    pass

class MealOut(BaseModel):
    Meal
    class Config:
        orm_model=True


class Daterange(BaseModel):
    # start_date: date
    # end_date: date
    start_date: datetime
    end_date: datetime