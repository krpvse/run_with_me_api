from sqlalchemy.exc import SQLAlchemyError, DBAPIError
from aioredis import RedisError
from smtplib import SMTPException
from celery.utils.log import get_task_logger

from app.logger import logger as fastapi_logger
celery_logger = get_task_logger(__name__)


def dao_error_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except (SQLAlchemyError, DBAPIError) as e:
            details = {'func_name': func.__name__, 'args': args, 'kwargs': kwargs}
            fastapi_logger.error(f'SQLAlchemy Exc: {e}\nDetails: {details}', exc_info=True)
    return wrapper


def redis_error_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except RedisError as e:
            details = {'func_name': func.__name__, 'args': args, 'kwargs': kwargs}
            fastapi_logger.error(f'Redis Exc: {e}\nDetails: {details}', exc_info=True)
    return wrapper


def smtp_error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except SMTPException as e:
            details = {'func_name': func.__name__, 'args': args, 'kwargs': kwargs}
            fastapi_logger.error(f'SMTP Exc: {e}\nDetails: {details}', exc_info=True)
    return wrapper