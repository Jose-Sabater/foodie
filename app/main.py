from fastapi import FastAPI
from .routers import meal
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app=FastAPI()
app.include_router(meal.router)


@app.get("/")
async def root():
    return {"message" : "Hello World"}

# if __name__=='__main__':
#     uvicorn.run(app)
# #Todo
"""
Be able to query for all meals inside a specific date, Schemas out and models
be able to query for all meals of a specific user
Add user login/tokenization
See all users
See current user_id
"""