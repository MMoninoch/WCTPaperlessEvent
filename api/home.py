# app/api/events.py
from io import BytesIO
from fastapi import APIRouter, HTTPException, Depends, Request, Query
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from database import SessionLocal
from database.models import Event
from sqlalchemy.orm import Session

router = APIRouter()
templates = Jinja2Templates(directory="templates")

items_per_page = 6

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/homepage/", response_class=HTMLResponse)
async def homepage(request: Request, page: int = Query(1, ge=1), db: Session = Depends(get_db)):
    items_per_page = 6
    offset = (page - 1) * items_per_page
    events = db.query(Event).limit(items_per_page).offset(offset).all()
    event_list = [event.as_dict() for event in events]

    return templates.TemplateResponse("homepage.html", {"request": request, "events": event_list, "page": page})

@router.get("/home/", response_class=HTMLResponse)
async def homepage(request: Request, page: int = Query(1, ge=1), db: Session = Depends(get_db)):
    items_per_page = 6
    offset = (page - 1) * items_per_page
    events = db.query(Event).limit(items_per_page).offset(offset).all()
    event_list = [event.as_dict() for event in events]

    return templates.TemplateResponse("home.html", {"request": request, "events": event_list, "page": page})

@router.get("/explore/", response_class=HTMLResponse)
async def explore(request: Request, page: int = Query(1, ge=1), db: Session = Depends(get_db)):
    items_per_page = 20
    offset = (page - 1) * items_per_page
    events = db.query(Event).limit(items_per_page).offset(offset).all()
    event_list = [event.as_dict() for event in events]

    return templates.TemplateResponse("explore.html", {"request": request, "events": event_list, "page": page})