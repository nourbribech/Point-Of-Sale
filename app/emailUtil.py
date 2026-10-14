from typing import List,Dict,Any

from fastapi import FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType, NameEmail
from pydantic import BaseModel
from starlette.responses import JSONResponse
from app.config import settings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
class EmailSchema(BaseModel):
    email: List[NameEmail]
    body: Dict[str, Any]

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=BASE_DIR / "templates",
)

app = FastAPI()


async def simple_send(email: EmailSchema) -> JSONResponse:
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.model_dump().get("email"),
        body="<p>Thanks for using Fastapi-mail</p>",
        subtype=MessageType.html,
    )
    await FastMail(conf).send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})
async def send_confirmation(to: str):
    message = MessageSchema(
        subject="Confirm your account",
        recipients=[to],
        body="<p>Welcome! Please confirm your account.</p>",
        subtype=MessageType.html,
    )
    await FastMail(conf).send_message(message)

async def send_with_template(to:str,variables:dict):

    message = MessageSchema(
        subject="mail de confirmation",
        recipients=[to,],
        template_body=variables,
        subtype=MessageType.html,
        )

    fm = FastMail(conf)
    await fm.send_message(message, template_name="test.html") 
    
