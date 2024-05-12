from email.message import EmailMessage
from smtplib import SMTP

from src.exceptions.error_handlers import smtp_error_handler
from src.settings import settings


@smtp_error_handler
def send_email(message_content: EmailMessage):
    server = SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
    server.starttls()
    server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
    server.send_message(message_content)
