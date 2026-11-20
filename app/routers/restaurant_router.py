from fastapi import Depends, APIRouter, HTTPException, Path
from typing import Annotated
from app.schemas.restaurant_schema import (CreateRestaurant, UpdateRestaurant, ResponseRestaurant, RestaurantDetail)
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.food_model import (Restaurant, User)
from app.database import get_session 
from app.core.dependencies import get_current_user

router = APIRouter(
    prefix = "/restaurant",
    tags = ["Restaurant"],
    dependencies = [Depends(get_current_user)]
)

@router.get("/", response_model = list[ResponseRestaurant], status_code = 200)
def get_all_restaurant(session: Session = Depends(get_session), current_user : User = Depends(get_current_user)):
    statement = select(Restaurant).where(current_user.id == Restaurant.owner_id)

    result = session.scalars(statement).all()
    return result

@router.post("/", response_model = ResponseRestaurant, status_code = 201)
def create_restaurant(restaurant_detail : CreateRestaurant, session : Session = Depends(get_session), current_user : User = Depends(get_current_user)):
    try:
        new_restaurant_data = Restaurant(
            name = restaurant_detail.name,
            location = restaurant_detail.location,
            owner_id = current_user.id
        )        
        session.add(new_restaurant_data)
        session.commit()
        session.refresh(new_restaurant_data)
        return new_restaurant_data
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to create restaurant"
        )

@router.patch("/{restaurant_id}", response_model = ResponseRestaurant, status_code = 200)
def update_restaurant(restaurant_id : Annotated[int, Path(gt = 0)], restaurant_detail : UpdateRestaurant, session : Session = Depends(get_session), current_user : User = Depends(get_current_user)):
    statement = select(Restaurant).where(Restaurant.id == restaurant_id, Restaurant.owner_id == current_user.id)
    restaurant = session.scalar(statement)

    if restaurant is None:
        raise HTTPException(status_code = 404, detail = f"No restaurant record found with id {restaurant_id}")

    restaurant.name = restaurant_detail.name
    restaurant.location = restaurant_detail.location

    session.commit()
    session.refresh(restaurant)
    return restaurant

@router.delete("/{restaurant_id}", status_code = 200)
def delete_restaurant(restaurant_id : Annotated[int, Path(gt = 0)], session : Session = Depends(get_session), current_user : User = Depends(get_current_user)):
    statement = select(Restaurant).where(Restaurant.id == restaurant_id, Restaurant.owner_id == current_user.id)
    restaurant = session.scalar(statement)

    if restaurant is None:
        raise HTTPException(status_code = 404, detail = f"No restaurant record found with id {restaurant_id}")

    session.delete(restaurant)
    session.commit()
    return {"message" : f"Successfully deleted the record of restaurant number {restaurant_id}"}

@router.get("/{restaurant_id}", response_model = RestaurantDetail, status_code = 200)
def get_restaurant_detail(restaurant_id : Annotated[int, Path(gt = 0)], session : Session = Depends(get_session), current_user : User = Depends(get_current_user)):
    statement = select(Restaurant).where(Restaurant.id == restaurant_id, Restaurant.owner_id == current_user.id)
    result = session.scalar(statement)

    if result is None:
        raise HTTPException(status_code = 404, detail = f"No restaurant record found with id {restaurant_id}")
    
    print(result.foods)
    print(len(result.foods))
    return result