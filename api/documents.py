# app/api/events.py
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/guidelines/", response_class=HTMLResponse)
async def index(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("guidelines.html", context)


@router.get("/term_of_service/", response_class=HTMLResponse)
async def term_of_service(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("terms_of_service.html", context)

@router.get("/faq/", response_class=HTMLResponse)
async def faq(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("faq.html", context)

@router.get("/user_documentation/", response_class=HTMLResponse)
async def user_documentation(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("user_documentation.html", context)