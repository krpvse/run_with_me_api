from fastapi import APIRouter, Response
from pydantic import UUID4

from app.auth.schemas import SUserAuth, SUserReg
from app.auth.auth import AccessToken, create_registration_confirmation_code
from app.profiles.dao import UsersDAO, RunnersDAO
from app.cache.cache import RegConfirmCodeCache
from app.tasks.tasks import send_registration_confirmation_email
from app.settings import settings
from app.exceptions import (InvalidEmailOrPasswordException, ExistingUserException,
                            NotExistingConfirmationCodeException, NotConfirmedEmailException)


router = APIRouter(
    prefix='/api/auth',
    tags=['Auth']
)


@router.post('/register')
async def register(user_data: SUserReg):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise ExistingUserException

    # add new user in database
    hashed_password = AccessToken.get_password_hash(user_data.password1)
    user_id = await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)
    await RunnersDAO.add(user_id=user_id, name=user_data.name)

    # send registration confirmation code to email
    confirmation_code = create_registration_confirmation_code()
    await RegConfirmCodeCache(code=confirmation_code, user_id=user_id, expire_time=600).save_code()

    send_registration_confirmation_email.delay(
        confirmation_link=f'{settings.DOMAIN_URL}{router.prefix}/confirmation/{user_id}/{confirmation_code}',
        email_to=user_data.email
    )

    return {'user_id': user_id, 'email': user_data.email, 'name': user_data.name, 'confirmation_code': confirmation_code}


@router.get('/confirmation/{user_id}/{confirmation_code}')
async def confirm_registration(user_id: int, confirmation_code: UUID4):
    code_from_cache = await RegConfirmCodeCache(code=confirmation_code, user_id=user_id).get_code()
    if not code_from_cache or code_from_cache != str(confirmation_code):
        raise NotExistingConfirmationCodeException

    await UsersDAO.update({'confirmed_email': True}, id=user_id)
    await RegConfirmCodeCache(code=confirmation_code, user_id=user_id).delete_code()
    return {'confirmed_email': True}


@router.post('/login')
async def login(response: Response, user_data: SUserAuth):
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if not user or not AccessToken.verify_password(user_data.password1, user.hashed_password):
        raise InvalidEmailOrPasswordException

    # check out email on confirmation, if email is not confirmed send letter to do it
    if not user.confirmed_email:
        confirmation_code = create_registration_confirmation_code()
        await RegConfirmCodeCache(code=confirmation_code, user_id=user.id, expire_time=600000).save_code()
        send_registration_confirmation_email.delay(
            confirmation_link=f'{settings.DOMAIN_URL}{router.prefix}/confirmation/{user.id}/{confirmation_code}',
            email_to=user_data.email
        )
        raise NotConfirmedEmailException

    access_token = AccessToken.create_token({'sub': str(user.id)})
    response.set_cookie('access_token', access_token, httponly=True)
    return {'user_id': user.id, 'access_token': access_token}


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie('access_token')
    return {'access_token': None}
