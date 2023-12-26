from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from api.core.security import oauth2_scheme, hash_password
from api.core.security import oauth2_scheme
from api.core.models import *
from api.core.security import JWTAuth

from api.users.routes import router as guest_router, user_router
from api.auth.routes import router
from api.mail.routes import mail_router
from api import events, qr_code, documents, home

app = FastAPI(docs_url="/docs")

# CORS settings
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication middleware
app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())

# Include routers
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(router)
app.include_router(mail_router)

# Include additional routers
app.include_router(events.router, prefix="/events", tags=["Event"])
app.include_router(qr_code.router, prefix="/qr_code", tags=["QR Code"])
app.include_router(documents.router, prefix="/documents", tags=["Document"])
app.include_router(home.router, prefix="/home", tags=["Home"])