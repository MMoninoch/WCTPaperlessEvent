from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl

mail_router =  APIRouter(
    prefix="/mail",
    tags=["Mail"],
    responses={404: {"description": "Not found"}},
)

class Email(BaseModel):
    recipient_email: str
    subject: str
    body: str

@mail_router.post("/send-email/")
def send_email(email: Email):
    sender_email = ''
    sender_password = 'qaht ctjl xnje dxml '
    
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = email.recipient_email
    message['Subject'] = email.subject

    message.attach(MIMEText(email.body, 'plain'))

    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email.recipient_email, message.as_string())
        return {"message": "Email sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")
