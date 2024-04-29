from smtplib import SMTP

from pydantic import EmailStr
from celery.utils.log import get_task_logger

from app.settings import settings
from app.tasks.celery_app import app
from app.tasks.email.templates import RegConfirmEmailMessage
from app.exceptions.error_handlers import smtp_error_handler

logger = get_task_logger(__name__)


@app.task
@smtp_error_handler
def send_registration_confirmation_email(
    confirmation_link: str,
    email_to: EmailStr
):

    message_content = RegConfirmEmailMessage(email_to, confirmation_link)

    server = SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
    server.starttls()
    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
    server.send_message(message_content)

    logger.info(f'Confirmation link is sent to email: {email_to}')
