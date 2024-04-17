from fastapi import APIRouter, Request, Form, status, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.users.router import register, login
from app.users.schemas import SUserAuth


router = APIRouter(
    tags=['Templates']
)

templates = Jinja2Templates('app/templates')


@router.get('/login')
async def login_page(
        request: Request
):
    return templates.TemplateResponse(name='login.html', context={'request': request})


@router.post('/submit-login-form')
async def login_page(
        response: Response,
        email: str = Form(),
        password1: str = Form()
):
    user_data = SUserAuth(email=email, password1=password1)
    await login(response=response, user_data=user_data)

    return RedirectResponse('/profile', status_code=status.HTTP_303_SEE_OTHER)


@router.get('/register')
async def register_page(
        request: Request
):
    return templates.TemplateResponse(name='register.html', context={'request': request})


@router.post('/submit-registration-form')
async def register_page(
        email: str = Form(),
        password1: str = Form(),
        password2: str = Form()
):
    user_data = SUserAuth(email=email, password1=password1, password2=password2)
    await register(user_data=user_data)

    return RedirectResponse('/login', status_code=status.HTTP_303_SEE_OTHER)


@router.get('/profile')
async def profile_page(
        request: Request
):
    return templates.TemplateResponse(name='profile.html', context={'request': request})
