from fastapi import APIRouter,HTTPException,Depends, Path, Query
from app.schemas.food_schema import (CreateFood, UpdateFood, ResponseFood)
from app.models.food_model import (Food, Restaurant, User)
from app.database import get_session
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Annotated
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix = "/foods",
    tags = ["Foods"]
)

@router.get("/", response_model = list[ResponseFood], status_code = 200)
def get_all_foods(session : Session = Depends(get_session), current_user : User = Depends(get_current_user)):
    statement = select(Food).join(Restaurant).where(Restaurant.owner_id == current_user.id)

    result = session.scalars(statement).all()
    return result
    
@router.get("/{food_id}", response_model = ResponseFood, status_code = 200)
def get_food(food_id : Annotated[int, Path(gt = 0)], session : Session = Depends(get_session), current_user : User = Depends(get_current_user)):

    statement = select(Food).join(Restaurant).where(food_id == Food.id, Restaurant.owner_id == current_user.id)

    result = session.scalar(statement)
    
    if result is None:
        raise HTTPException(status_code = 404, detail = f"No food data found with food_id {food_id}")
    
    return result

@router.post("/", response_model = ResponseFood, status_code = 201)
def create_food(food : CreateFood, session : Session = Depends(get_session), current_user : User = Depends(get_current_user) ):
    statement = select(Restaurant).where(
        Restaurant.id == food.restaurant_id, 
        current_user.id == Restaurant.owner_id
    )
    restaurant = session.scalar(statement)
    if restaurant is None:
        raise HTTPException(status_code = 404, detail = "No restaurant detail found")
    
    new_food_detail = Food(
        name = food.name,
        description = food.description,
        price = food.price,
        restaurant_id = food.restaurant_id,
        category = food.category
    )
    session.add(new_food_detail)
    session.commit()
    session.refresh(new_food_detail)
    return new_food_detail
        
@router.patch("/{food_id}", response_model = ResponseFood, status_code = 200)
def update_food(food_id : Annotated[int, Path(gt = 0)], food_data : UpdateFood, session : Session = Depends(get_session), current_user : User = Depends(get_current_user)):
    statement = select(Food).join(Restaurant).where(food_id == Food.id ,Restaurant.owner_id == current_user.id)    
    result = session.scalar(statement)

    if result is None:
        raise HTTPException(status_code = 404, detail = f"No food data found with food_id {food_id}")
    
    for key, value in food_data.model_dump(exclude_unset = True, exclude_none = True).items():
        setattr(result, key, value)

    session.commit()
    session.refresh(result)
    
    return result

@router.delete("/{food_id}", status_code = 200)
def delete_food(food_id : Annotated[int, Path(gt = 0)], session : Session = Depends(get_session), current_user : User = Depends(get_current_user)):
    
    statement = select(Food).join(Restaurant).where(Food.id == food_id, Restaurant.owner_id == current_user.id)
    result = session.scalar(statement)
    
    if result is None:
        raise HTTPException(status_code = 404, detail = f"No food data found with food_id {food_id}")
    session.delete(result)
    session.commit()
    return {
        "message" : f"successfully deleted food record of {food_id}"
    }
