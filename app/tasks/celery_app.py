from celery import Celery

from app.settings import settings


app = Celery(
    'tasks',
    broker=settings.REDIS_URL,
    include=['app.tasks.tasks']
)
