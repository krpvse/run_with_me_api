from fastapi import APIRouter, Response, Depends
from pydantic import UUID4

from app.auth.schemas import SUserAuth, SUserReg
from app.auth import utils as auth_utils
from app.auth.token import create_tokens, recreate_tokens
from app.profiles.dao import UsersDAO, RunnersDAO
from app.cache.cache import RegConfirmCodeCache
from app.tasks.tasks import send_registration_confirmation_email
from app.settings import settings
from app.logger import logger
from app.exceptions.exceptions import (
    InvalidEmailOrPasswordException,
    ExistingUserException,
    NotExistingConfirmationCodeException,
    NotConfirmedEmailException
)


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
    hashed_password = auth_utils.get_password_hash(user_data.password1)
    user_id = await UsersDAO.add_one(email=user_data.email, hashed_password=hashed_password)
    await RunnersDAO.add_one(user_id=user_id, name=user_data.name)
    logger.info(f'New user has registered without email confirmation: id{user_id}')

    # send registration confirmation code to email
    confirm_code, confirm_link = await auth_utils.create_confirmation_code(
        api_url=f'{settings.DOMAIN_URL}{router.prefix}/confirmation/',
        user_id=user_id,
        to_cache=True
    )
    send_registration_confirmation_email.delay(confirmation_link=confirm_link, email_to=user_data.email)

    return {
        'msg': 'Success! User is registered',
        'user_id': user_id,
        'email': user_data.email,
        'name': user_data.name,
        'confirmation_code': confirm_code
    }


@router.get('/confirmation/{user_id}/{confirmation_code}')
async def confirm_registration(user_id: int, confirmation_code: UUID4):
    code_from_cache = await RegConfirmCodeCache(code=confirmation_code, user_id=user_id).get_code()
    if not code_from_cache or code_from_cache != str(confirmation_code):
        raise NotExistingConfirmationCodeException

    await UsersDAO.update({'confirmed_email': True}, id=user_id)
    await RegConfirmCodeCache(code=confirmation_code, user_id=user_id).delete_code()
    logger.info(f'User confirmed email: id{user_id}')

    return {'msg': 'Success! Email is confirmed'}


@router.post('/update-jwt')
def update_jwt_cookies_depends_on_refresh_token(
        response: Response,
        tokens: tuple = Depends(recreate_tokens)
):
    access_token = tokens[0]
    refresh_token = tokens[1]
    response.set_cookie('access_token', access_token, httponly=True)
    response.set_cookie('refresh_token', refresh_token, httponly=True)
    return {
        'msg': 'Tokens is recreated',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer'
    }


@router.post('/login')
async def login(response: Response, user_data: SUserAuth):
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if not user or not auth_utils.verify_password(user_data.password1, user.hashed_password):
        raise InvalidEmailOrPasswordException

    # check out email on confirmation, if email is not confirmed send letter to do it
    if not user.confirmed_email:
        confirm_code, confirm_link = await auth_utils.create_confirmation_code(
            api_url=f'{settings.DOMAIN_URL}{router.prefix}/confirmation/',
            user_id=user.id,
            to_cache=True
        )
        send_registration_confirmation_email.delay(confirmation_link=confirm_link, email_to=user_data.email)
        raise NotConfirmedEmailException

    access_token, refresh_token = await create_tokens({'sub': str(user.id)})
    response.set_cookie('access_token', access_token, httponly=True)
    response.set_cookie('refresh_token', refresh_token, httponly=True)

    logger.debug(f'User is logged in: id{user.id}')

    return {
        'msg': 'User is authenticated',
        'user_id': user.id,
        'access_token': access_token,
        'refresh_token': refresh_token,
        'token_type': 'Bearer'
    }


@router.post('/logout')
async def logout(response: Response):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return {'msg': 'User is logout'}
