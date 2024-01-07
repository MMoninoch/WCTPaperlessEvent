import os
from typing import Annotated
from fastapi import APIRouter, Form, HTTPException, Request, status, Depends, Header
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from ..core.security import JWTAuth, get_current_user, verify_password
from api.core.schemas import Token, User, UserResponse
from ..core.database import get_db
from .auth import _get_user_token, get_token, get_refresh_token
from ..core.models import *


router =  APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)

db_dependency = Annotated[Session, Depends(get_db)]


# @router.post("/token", status_code=status.HTTP_200_OK)
# async def authenticate_user(db: db_dependency, data: OAuth2PasswordRequestForm = Depends()):
#     return await get_token(db=db, data=data)

@router.post("/token", status_code=status.HTTP_200_OK)
async def authenticate_user(
    email: str = Form(...),
    password: str = Form(...),
    refresh_token: str = Form(...),
    db: Session = Depends(get_db)
):
    # Retrieve the user from the database based on the provided email
    user = db.query(UserModel).filter(UserModel.email == email).first()

    # Check if the user exists and verify the password
    if user and verify_password(password, user.hashed_password):
        # Password is correct, generate token
        token_data = await _get_user_token(user=user, refresh_token=refresh_token)
        redirect_url = "/home/home"
        return RedirectResponse(redirect_url, status_code=302)

    # If the user does not exist or the password is incorrect, raise an HTTPException
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")



    
