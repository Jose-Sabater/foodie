from sqlalchemy import create_engine
import pandas as pd
import psycopg2
from .config import settings
SQLALCHEMY_DATABASE_URL=f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine= create_engine(SQLALCHEMY_DATABASE_URL)



df=pd.read_csv('food_database\\calories.csv')
df['per100grams'][df['per100grams']=='100g'] = 'g'
df['per100grams'][df['per100grams']=='100ml'] = 'ml'

df.drop(columns=['KJ_per100grams','per100grams'],inplace=True)
df['FoodCategory']=df['FoodCategory'].str.lower()
df['FoodItem']=df['FoodItem'].str.lower()
df.rename(columns={'Cals_per100grams' : 'cals_pergram'}, inplace=True)
df['cals_pergram']=df['cals_pergram'].str.replace(" cal","")
df['cals_pergram']=df['cals_pergram'].astype(int)/100
print(df)




df.to_sql('food_calories', engine)