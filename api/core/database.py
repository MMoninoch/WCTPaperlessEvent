from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from typing import Generator
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:123@localhost:3306/event_db"

engine = create_engine(
    DATABASE_URL, pool_pre_ping=True, pool_recycle=300, pool_size=5, max_overflow=0)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
