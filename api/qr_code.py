from fastapi import APIRouter, File, UploadFile, Request, HTTPException, Depends
from fastapi.responses import StreamingResponse, JSONResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
from io import BytesIO
from pydantic import BaseModel
import validators
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/qr_code/", response_class=HTMLResponse)
async def qr_code(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("qr_code.html", context)

class QrCodeData(BaseModel):
    data: str

