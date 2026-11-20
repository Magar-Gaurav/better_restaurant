from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Annotated

class UserCreate(BaseModel):
    username : Annotated[str, Field(min_length = 3, max_length = 100, description = "User name")]

    email : EmailStr

    password : Annotated[str, Field(min_length = 8, max_length = 128, description = "User password")]

class UserResponse(BaseModel):
    id : int
    username : str
    email : EmailStr
    is_active : bool

    model_config = ConfigDict(from_attributes = True)

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username : str | None = None