from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated


class CreateFood(BaseModel):
    name : Annotated[str, Field(description = "Food Name", min_length = 3, max_length = 100)]
    description : Annotated[str, Field(description = "Food Description",min_length = 5, max_length = 500)]
    price : Annotated[float, Field(description = "Food Price", gt = 0, le = 1000)]
    restaurant_id : Annotated[int, Field(description = "Restaurant Id", gt = 0)]
    category : Annotated[str, Field(description = "Food category", min_length = 3)]

class UpdateFood(BaseModel):
    name : Annotated[str | None, Field(min_length = 3, max_length = 50)] = None
    description : Annotated[str | None, Field(min_length = 3, max_length = 1000)] = None
    price : Annotated[float | None, Field(gt = 0, le = 1000)] = None
    category : Annotated[str | None, Field(min_length = 3)] = None

class ResponseFood(BaseModel):
    model_config = ConfigDict(from_attributes = True)

    id : int
    name : str
    category : str
    description : str
    price : float
    restaurant_id : int

class FoodSummary(BaseModel):
    id : int
    name : str
    category : str
    model_config = ConfigDict(from_attributes = True)