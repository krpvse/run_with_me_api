from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.profiles.router import router as profiles_router
from app.auth.router import router as auth_router
from app.pages.router import router as pages_router


app = FastAPI()


app.mount('/static', StaticFiles(directory='app/static'), 'static')


app.include_router(auth_router)
app.include_router(profiles_router)
app.include_router(pages_router)
