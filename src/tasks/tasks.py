import asyncio
import datetime

from celery.schedules import crontab
from celery.utils.log import get_task_logger
from pydantic import EmailStr

from src.auth.utils import create_confirmation_code
from src.profiles.dao import RunnersDAO, UsersDAO
from src.settings import settings
from src.tasks.celery_app import app
from src.tasks.email.tasks import send_email
from src.tasks.email.templates import RegConfirmEmailMessage, RemindConfirmEmailMessage


logger = get_task_logger(__name__)

loop = asyncio.get_event_loop()


@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour='0', minute='0'), check_unconfirmed_users.s())


@app.task
def check_unconfirmed_users():
    """
    Get all users who did not confirm email:
    - if time is expired then delete user;
    - if time is not expired, send confirmation email to remind
    """

    current_date = datetime.datetime.utcnow()
    unconfirmed_users = loop.run_until_complete(UsersDAO.find(confirmed_email=False))

    if not unconfirmed_users:
        logger.info('Unconfirmed users was checked. All is confirmed!')
        return

    for user in unconfirmed_users:
        registration_timedelta = current_date - user.registration_date

        if registration_timedelta > datetime.timedelta(days=2):
            loop.run_until_complete(RunnersDAO.delete(id=user.id))
            user_id = loop.run_until_complete(UsersDAO.delete(id=user.id))
            if user_id:
                logger.info(f'Time of email confirmation expired, user is deleted: {user.email}')
        else:
            confirm_code, confirm_link = loop.run_until_complete(create_confirmation_code(
                api_url=f'{settings.DOMAIN_URL}/api/auth/confirmation/',
                user_id=user.id,
                to_cache=True
            ))
            message_content = RemindConfirmEmailMessage(email_to=user.email, confirmation_link=confirm_link)
            response = send_email(message_content)
            if not isinstance(response, Exception):
                logger.info(f'Send email to remind about registration confirmation: {user.email}')


@app.task
def send_registration_confirmation_email(
    confirmation_link: str,
    email_to: EmailStr
):
    message_content = RegConfirmEmailMessage(email_to, confirmation_link)
    response = send_email(message_content)
    if not isinstance(response, Exception):
        logger.info(f'Confirmation link is sent to email: {email_to}')
    else:
        logger.error(f'Confirmation link is NOT sent to email: {email_to}')
