import io
from databases import Database
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, FileResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, models, schemas
from database.schemas import EventBase, EventCreate, EventInDB, EventPublic, EventUpdate
from database.models import Event
from datetime import datetime
from fastapi import APIRouter, HTTPException, Request, Form, Depends, UploadFile, File, Path, status
from typing import Optional
import base64
from typing import List
from sqlalchemy.sql import func

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/api/event/", response_class=HTMLResponse)
async def event_submission_form(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("event_submission_form.html", context)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/api/events/", response_model=List[EventPublic])
def get_all_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return events


@router.post("/api/events/", response_model=EventPublic)
def create_event_with_image(
    request: Request,
    event_name: str = Form(...),
    event_datetime: datetime = Form(...),
    event_location: str = Form(...),
    event_description: str = Form(...),
    event_photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Ensure that the image data is properly encoded (base64).
    image_data = base64.b64encode(event_photo.file.read())

    event_data = EventCreate(
        title=event_name,
        description=event_description,
        date_time=event_datetime,
        location=event_location
    )

    db_event = Event(
        title=event_data.title,
        description=event_data.description,
        date_time=event_data.date_time,
        location=event_data.location,
        image=image_data
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    # Render the template with the event data
    return templates.TemplateResponse("event_template.html", {"request": request, "event": db_event})


@router.get("/api/event/{event_id}", response_model=EventPublic)
def get_event_by_id(event_id: int, db: Session = Depends(get_db)):
    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.get("/api/events/{title}", response_class=HTMLResponse)
def get_event_template(title: str, request: Request, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.title == title).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    # Set content type explicitly
    return templates.TemplateResponse("event_template.html", {"request": request, "event": db_event}, media_type="text/html")


@router.get("/api/events/{title}/image")
def get_event_image(title: str, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.title == title).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")

    decoded_image = base64.b64decode(db_event.image)
    # Set the content type to image/png
    headers = {"Content-Type": "image/png"}

    return StreamingResponse(io.BytesIO(decoded_image), media_type="image/png", headers=headers)

@router.put("/api/events/{event_id}/update", response_model=EventPublic)
def update_event_by_id(
    request: Request,
    event_id: int,
    event_name: str = Form(...),
    event_datetime: datetime = Form(...),
    event_location: str = Form(...),
    event_description: str = Form(...),
    event_photo: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Check if the event with the given ID exists
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Ensure that the image data is properly encoded (base64).
    image_data = base64.b64encode(event_photo.file.read())

    # Update the event with the new data
    db_event.title = event_name
    db_event.date_time = event_datetime
    db_event.location = event_location
    db_event.description = event_description
    db_event.image = image_data

    # Commit the changes to the database
    db.commit()
    db.refresh(db_event)

    # Render the template with the updated event data
    return templates.TemplateResponse("event_template.html", {"request": request, "event": db_event})


@router.delete("/api/events/{event_id}/delete", response_model=dict)
def delete_event_by_id(
    event_id: int,
    db: Session = Depends(get_db)
):
    # Check if the event with the given ID exists
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")

    # Delete the event from the database
    db.delete(db_event)
    db.commit()

    # Return a simple JSON response
    return {"detail": "Event deleted successfully"}