from fastapi import Depends, APIRouter, HTTPException, Path
from typing import Annotated
from app.schemas.user_schema import (UserCreate, UserResponse)
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.food_model import User
from app.database import get_session 
from app.core.security import hash_password

from datetime import timedelta

from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user_schema import Token
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.core.dependencies import get_current_user

from configs.config import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(
    prefix = "/auth",
    tags = ["User Authentication"]
)

@router.post("/register", response_model = UserResponse, status_code = 201)
def register_user(user_data : UserCreate, session : Session = Depends(get_session)):
    statement = select(User).where(
        User.username == user_data.username
    )
    existed_username = session.scalar(statement)

    if existed_username:
        raise HTTPException(
            status_code = 409, detail = "Username already registered"
        )
    
    statement = select(User).where(
        User.email == user_data.email
    )
    existing_email = session.scalar(statement)

    if existing_email:
        raise HTTPException(
            status_code = 409, detail = "Email already registered"
        )

    hashed_password = hash_password(user_data.password)

    new_user = User(
        username = user_data.username,
        email = user_data.email,
        hashed_password = hashed_password 
    )
    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    except Exception:
        session.rollback()
        raise
    return new_user

@router.post("/login", response_model = Token)
def login_user(form_data : OAuth2PasswordRequestForm = Depends(), session : Session = Depends(get_session)):
    statement = select(User).where(User.username == form_data.username)

    user = session.scalar(statement)

    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code = 401, detail = "Invalid username or password", headers = {"WWW-Authenticate" : "Bearer"})
    
    if not user.is_active:
        raise HTTPException(status_code = 400, detail = "Inactive user")

    access_token_expires = timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data = {"sub" : user.username}, expires_delta = access_token_expires
    )

    return{
        "access_token" : access_token,
        "token_type" : "bearer"
    }

@router.get("/me", response_model = UserResponse)
def get_logged_in_user(current_user : User = Depends(get_current_user)):
    return current_user