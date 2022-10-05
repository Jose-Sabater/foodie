""" Main module for the application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import meal, auth, user
from . import models
from .database import engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(meal.router)
app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
async def root() -> dict:
    """Check main health of website"""
    return {"message": "Hello World"}

# if __name__=='__main__':
#     uvicorn.run(app)
