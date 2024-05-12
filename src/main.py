from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.auth.router import router as auth_router
from src.logger import logger, setup_logging
from src.profiles.router import router as profiles_router


app = FastAPI()


app.mount('/static', StaticFiles(directory='src/static'), 'static')


app.include_router(auth_router)
app.include_router(profiles_router)


@app.on_event('startup')
def startup():
    setup_logging()
    logger.info('App is started')


@app.on_event('shutdown')
def shutdown():
    logger.info('App is stopped')
