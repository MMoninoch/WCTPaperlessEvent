from fastapi import HTTPException
from ..core.models import UserModel
from ..core.security import hash_password
from datetime import datetime


async def register_user(data, db):
    existing_user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = UserModel(
        username = data.username,
        first_name = data.first_name,
        last_name = data.last_name,
        email = data.email,
        hashed_password = hash_password(data.hashed_password),
        registered_at = datetime.now(),
        updated_at = datetime.now()
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
