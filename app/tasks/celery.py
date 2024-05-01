import celery

from app.settings import settings
from app.logger import setup_logging


app = celery.Celery(
    'tasks',
    broker=settings.REDIS_URL,
    include=['app.tasks.tasks'],

)

app.conf.broker_connection_retry_on_startup = True
app.conf.timezone = 'Europe/Moscow'


@celery.signals.setup_logging.connect
def on_setup_logging(**kwargs):
    setup_logging()
