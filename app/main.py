from fastapi import FastAPI
from .routers import meal, auth, user
from . import models
from .database import engine
from fastapi.templating import Jinja2Templates

models.Base.metadata.create_all(bind=engine)

app=FastAPI()
app.include_router(meal.router)
app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message" : "Hello World"}

# if __name__=='__main__':
#     uvicorn.run(app)
# #Todo
"""
Add a column for amount of registered posts
be able to query for all meals of a specific user
See all users
Add alembic
Add jinja2 templates /frontend
add separate flask frontend folder that calls our APIs
"""