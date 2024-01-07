from pydantic import BaseModel, EmailStr
from typing import Optional, Union
from datetime import datetime

class User(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    hashed_password: str
    
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
    expires_in: int


class Baseresponse(BaseModel):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        
class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    registered_at: Union[None, datetime] = None

class UserLogin(BaseModel):
    email: str
    hashed_password: str