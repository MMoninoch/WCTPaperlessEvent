from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from fastapi import FastAPI
from fastapi import FastAPI

app = FastAPI()

app = FastAPI()

DATABASE_URL = 'mysql+mysqlconnector://root:123@localhost:3306/event_db'
engine = create_engine(DATABASE_URL, echo=True)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine)