import celery

from src.logger import setup_logging
from src.settings import settings


app = celery.Celery(
    'tasks',
    broker=settings.REDIS_URL,
    include=['src.tasks.tasks'],

)

app.conf.broker_connection_retry_on_startup = True
app.conf.timezone = 'Europe/Moscow'


@celery.signals.setup_logging.connect
def on_setup_logging(**kwargs):
    setup_logging()
