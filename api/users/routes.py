import logging
from sqlite3 import IntegrityError
from typing import Annotated
from fastapi import APIRouter, Form, HTTPException, Request, status, Depends
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from requests import request
from sqlalchemy.orm import Session

from api.auth.auth import _get_user_token
from ..core.database import get_db
from ..core.schemas import Token, User, UserResponse
from .register import register_user
from ..core.models import *
from ..core.security import JWTAuth, create_access_token, get_current_user, get_token_payload, hash_password, oauth2_scheme, verify_password
from fastapi.templating import Jinja2Templates
from starlette.authentication import AuthCredentials



router =  APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

user_router =  APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)


templates = Jinja2Templates(directory="templates")


db_dependency = Annotated[Session, Depends(get_db)]


# @router.post('', status_code=status.HTTP_201_CREATED)
# async def create_table(user: User, db: db_dependency):
#     db_user = UserModel(
#         username = user.username,
#         first_name = user.first_name,
#         last_name = user.last_name,
#         email = user.email,
#         hashed_password = hash_password(user.hashed_password),
#         registered_at = datetime.now(),
#         updated_at = datetime.now()
#     )
#     db.add(db_user)
#     db.commit()


@router.get("/register_page", response_class=HTMLResponse)
async def register(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("register.html", context)

@router.get("/login_page", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})





@router.post('/register_page', response_class=HTMLResponse)
async def create_user_form(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    hashed_password: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        existing_user = db.query(UserModel).filter(UserModel.email == email).first()
        if existing_user:
            error_message = "Email already registered"
            return templates.TemplateResponse("register.html", {"request": request, "message": error_message})

        new_user = UserModel(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            hashed_password=hash_password(hashed_password),
            registered_at=datetime.now(),
            updated_at=datetime.now()
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return RedirectResponse(url="../../home/home", status_code=303)
    except Exception as e:
        db.rollback()
        error_message = f"Failed to register user: {str(e)}"
        return templates.TemplateResponse("register.html", {"request": request, "message": error_message})




# @router.post('/register', status_code=status.HTTP_201_CREATED)
# async def create_user(data: User, db: db_dependency):
#     await register_user(data=data, db=db)
#     payload = {"message": "User account has been succesfully created."}
#     return JSONResponse(content=payload)

# @user_router.post('/me', status_code=status.HTTP_200_OK, response_model=UserResponse)
# def get_user_detail(request: Request):
#     return request.user
