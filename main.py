from fastapi import FastAPI
from app.routers import (food_router, restaurant_router, user_router)
from app.database import Base, engine
from app.models.food_model import Food, Restaurant, User

app = FastAPI(
    title = "Food Management API",
    summary = "API which handles restaurant and food"
)

app.include_router(food_router.router)
app.include_router(restaurant_router.router)
app.include_router(user_router.router)

# Base.metadata.create_all(engine)

@app.get("/")
def home():
    return {
        "Food Management API" : "Food and Restaurant data"
    }