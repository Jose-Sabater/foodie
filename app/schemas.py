"""Main schema module"""
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class MealBase(BaseModel):
    meal: str
    quantity: int

    class Config:
        orm_model = True


class Meal(MealBase):
    calories_consumed: float
    meal_id: int
    date: datetime

    class Config:
        orm_mode = True


class MealCreate(MealBase):
    pass


class MealOut(BaseModel):
    Meal: Meal
    votes: int

    class Config:
        orm_model = True


class Daterange(BaseModel):
    # start_date: date
    # end_date: date
    start_date: datetime
    end_date: datetime


class UserLogin (BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
