import base64
from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    date_time: datetime
    location: str
    image: Optional[bytes] = None

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    pass

class EventInDB(EventBase):
    id: int

    class Config:
        orm_mode = True

class EventPublic(EventInDB):
    image_base64: Optional[str] 

    @property
    def image_base64(self):
        if self.image:
            return base64.b64encode(self.image).decode('utf-8')
        return None

