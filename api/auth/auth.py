from fastapi import HTTPException
from datetime import timedelta

from requests import Session

from api.core.database import SessionLocal
from ..core.security import verify_password, get_token_payload, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, create_refresh_token
from ..core.schemas import Token
from ..core.models import UserModel

async def get_token(db, data):
    user = db.query(UserModel).filter(UserModel.email == data.get('email')).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email is not registered.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not verify_password(data.get('password'), user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Invalid Login Credentials.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return await _get_user_token(user=user)
        

  
async def get_refresh_token(db: Session, token: str):
    try:
        payload = get_token_payload(token=token)
    
        # Check if payload is None and handle the case
        if payload is None:
            # Handle the error or raise an exception
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id = payload.get('id', None)

        # Assuming you have a User model
        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token: User not found.",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return await _get_user_token(user=user, refresh_token=token)
    except Exception as e:
        print(f"Error in get_refresh_token: {e}")
        raise





    
    
async def _get_user_token(user: UserModel, refresh_token=None):
    payload = {"id": user.id}
    
    access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = await create_access_token(payload, access_token_expire)
    if not refresh_token:
        refresh_token = await create_refresh_token(payload)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expire.seconds  # in seconds
    )




# async def _get_user_token(user: UserModel, refresh_token = None):
#     payload = {"id": user.id}
    
#     access_token_expire = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
#     access_token = await create_access_token(payload, access_token_expire)
#     if not refresh_token:
#         refresh_token = await create_refresh_token(payload)
#     return Token(
#         access_token=access_token,
#         refresh_token=refresh_token,
#         expires_in=access_token_expire.seconds # in second
#     )