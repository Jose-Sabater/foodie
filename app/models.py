from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, Numeric, SmallInteger, String, Float
#good practice to record when things are created

class Meal(Base):
    __tablename__ = "meals"
    meal_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer,  nullable=False)
    meal = Column(String, nullable=False)
    quantity = Column(SmallInteger, nullable=False)
    calories_consumed = Column(Float,nullable=False)
    date = Column(TIMESTAMP (timezone=True), nullable=False, server_default=text('now()'))

class Calories(Base):
    __tablename__ = "food_calories"
    index = Column(Integer, primary_key=True, nullable=False)
    foodcategory = Column(String,  nullable=False)
    fooditem = Column(String, nullable=False)
    cals_pergram = Column(Float, nullable=False)


class User(Base):
    __tablename__ = "users"
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP (timezone=True),
                         nullable=False, server_default=text('now()'))

