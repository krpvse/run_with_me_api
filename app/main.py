from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.profiles.router import router as profiles_router
from app.auth.router import router as auth_router
from app.pages.router import router as pages_router
from app.logger import setup_logging, logger


app = FastAPI()


app.mount('/static', StaticFiles(directory='app/static'), 'static')


app.include_router(auth_router)
app.include_router(profiles_router)
app.include_router(pages_router)


@app.on_event('startup')
def startup():
    setup_logging()
    logger.info('App is started')


@app.on_event('shutdown')
def shutdown():
    logger.info('App is stopped')
