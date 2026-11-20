from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated
from app.schemas.food_schema import FoodSummary

class CreateRestaurant(BaseModel):
    name : Annotated[str, Field(description = "Restaurant Name", min_length = 3, max_length = 50)]
    location : Annotated[str, Field(description = "Restaurant Location", min_length = 3, max_length = 50)]

class UpdateRestaurant(BaseModel):
    name : str | None = None
    location : str | None = None

class ResponseRestaurant(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    id : int
    name : str
    location : str
    owner_id : int

class RestaurantDetail(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    id : int
    name : str
    location : str
    foods: list[FoodSummary]
