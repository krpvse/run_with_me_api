import shutil

from fastapi import APIRouter, Request, Form, status, Response, Depends, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from app.auth.router import register, login
from app.auth.schemas import SUserAuth, SUserReg

from app.profiles.router import get_profile_info, edit_profile
from app.profiles.dto import UserDTO
from app.profiles.schemas import SProfile

from app.dependencies.common import disallow_without_owner_permissions, check_owner_permissions


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
    result = await login(response=response, user_data=user_data)
    user_id = result['user_id']
    token = result['access_token']

    redirect_response = RedirectResponse(f'/profile/{user_id}', status_code=status.HTTP_303_SEE_OTHER)
    redirect_response.set_cookie('access_token', token, httponly=True)
    return redirect_response


@router.get('/register')
async def register_page(
        request: Request
):
    return templates.TemplateResponse(name='register.html', context={'request': request})


@router.post('/submit-registration-form')
async def register_page(
        email: str = Form(),
        name: str = Form(),
        password1: str = Form(),
        password2: str = Form()
):
    user_data = SUserReg(email=email, name=name, password1=password1, password2=password2)
    await register(user_data=user_data)

    return RedirectResponse('/login', status_code=status.HTTP_303_SEE_OTHER)


@router.get('/profile/{profile_id}')
async def profile_page(
        request: Request,
        profile: UserDTO = Depends(get_profile_info),
        has_owner_permissions: bool = Depends(check_owner_permissions),
):
    form = {
        'action': f'/submit-profile-form-{profile.id}' if has_owner_permissions else f'/suggest-to-run-{profile.id}',
        'input_mode': 'enabled' if has_owner_permissions else 'disabled',
        'button_name': 'Сохранить' if has_owner_permissions else 'Предложить побегать',
    }

    context = {
        'request': request,
        'profile': profile,
        'form': form,
        'has_owner_permissions': has_owner_permissions,
    }

    return templates.TemplateResponse(name='profile.html', context=context)


@router.post('/submit-profile-form-{profile_id}', dependencies=[Depends(disallow_without_owner_permissions)])
async def profile_page(
        profile_id: int,
        image: UploadFile,
        name: str = Form(),
        age: int = Form(),
        description: str = Form(),
        distance_from: int = Form(),
        distance_to: str = Form(),
        speed_from: int = Form(),
        speed_to: int = Form(),
):
    update_data = SProfile(
        name=name,
        age=age,
        description=description,
        distance_from=distance_from,
        distance_to=distance_to,
        speed_from=speed_from,
        speed_to=speed_to
    )

    if image.filename:
        with open(f'app/static/images/profile-images/profile{profile_id}.webp', 'wb+') as file_obj:
            shutil.copyfileobj(image.file, file_obj)
    await edit_profile(profile_id=profile_id, update_data=update_data)

    return RedirectResponse(f'/profile/{profile_id}', status_code=status.HTTP_303_SEE_OTHER)
