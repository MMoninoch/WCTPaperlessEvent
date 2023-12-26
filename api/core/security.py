from fastapi import Depends, HTTPException, Request, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta, datetime
from jose import JWTError, jwt
from requests import Session
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from .models import UserModel
from .database import get_db

SECRET_KEY = "6da7226fc8b5ded1db89f999299b12b0ccfff72d6a81573a5f3f20f677c258c6"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

async def create_access_token(data, expire: timedelta):
    payload = data.copy()
    expires_in = datetime.utcnow() + expire
    payload.update({"exp": expires_in})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def create_refresh_token(data):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_token_payload(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
    return payload


def get_current_user(token: str = Depends(oauth2_scheme)) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = {"sub": username}
    except JWTError:
        raise credentials_exception
    return token_data



# class JWTAuth:
    
#     async def authenticate(self, conn):
#         guest = AuthCredentials(['unauthenticated']), UnauthenticatedUser()
        
#         if 'authorization' not in conn.headers:
#             return guest
        
#         token = conn.headers.get('authorization').split(' ')[1]
#         if not token:
#             return guest
        
#         user = get_current_user(token=token)
        
#         if not user:
#             return guest
        
#         return AuthCredentials('authenticated'), user

class JWTAuth:
    
    async def authenticate(self, request: Request, db: Session = Depends(get_db)):
        guest = AuthCredentials(['unauthenticated']), UnauthenticatedUser()
        
        if 'authorization' not in request.headers:
            return guest
        
        token = request.headers.get('authorization').split(' ')[1]
        if not token:
            return guest
        
        user = get_current_user(token=token, db=db)
        
        if not user:
            return guest
        
        return AuthCredentials('authenticated'), user
