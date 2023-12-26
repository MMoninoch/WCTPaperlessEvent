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

# QR Code endpoints
@router.post("/api/generate-qr-code/")
async def generate_qr_code_endpoint(qr_code_data: QrCodeData):
    
    # QR Code generation and scanning
    def generate_qr_code(data: str) -> Image.Image:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        return img
    
    qr_code = generate_qr_code(qr_code_data.data)
    
    img_bytes = BytesIO()
    qr_code.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return StreamingResponse(content=img_bytes, media_type="image/png")





@router.post("/api/upload-qr-code/")
async def upload_qr_code(qr_code_file: UploadFile = File(...)):
    try:
        # Check if the uploaded file is an image
        if not qr_code_file.content_type.startswith("image/"):
            raise HTTPException(status_code=415, detail="Invalid media type; only images are supported")

        # Read the contents of the file
        qr_code_content = qr_code_file.file.read()

        # Decode the QR code content
        decoded_qr_codes = decode(Image.open(BytesIO(qr_code_content)))

        if not decoded_qr_codes:
            raise HTTPException(status_code=400, detail="No QR code found in the provided image")

        decoded_url = decoded_qr_codes[0].data.decode('utf-8')

        # Validate and sanitize the decoded URL
        if not validators.url(decoded_url):
            raise HTTPException(status_code=400, detail="Invalid URL decoded from QR code")

        # Return the decoded URL in the response
        response_content = {"decoded_url": decoded_url}

        # Redirect to the decoded URL
        redirect_response = RedirectResponse(url=decoded_url)

        return JSONResponse(content=response_content, headers=redirect_response.headers)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing QR code: {str(e)}")


