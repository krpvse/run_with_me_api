import smtplib

from pydantic import EmailStr

from app.tasks.celery_app import app
from app.tasks.email.templates import RegConfirmEmailMessage
from app.settings import settings


@app.task
def send_registration_confirmation_email(
    confirmation_link: str,
    email_to: EmailStr
):

    message_content = RegConfirmEmailMessage(email_to, confirmation_link)

    server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
    server.starttls()
    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)

    server.send_message(message_content)
