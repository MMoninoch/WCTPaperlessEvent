from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
import base64

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    date_time = Column(DateTime)
    location = Column(String)
    image = Column(LargeBinary)

    def __init__(self, title, description, date_time, location, image):
        self.title = title
        self.description = description
        self.date_time = date_time
        self.location = location
        self.image = image
        
    def as_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date_time": self.date_time,
            "location": self.location,
            "image_base64": base64.b64encode(self.image).decode('utf-8') if self.image else None
        }