from datetime import datetime, timedelta

import jwt
from fastapi import Request, HTTPException

from app.settings import settings
from app.auth.dao import RefreshJWTDAO
from app.profiles.dao import UsersDAO
from app.exceptions.exceptions import (
    FailedToCreateTokenException,
    InvalidTokenException,
    UserDoesNotExistException,
    ExpiredTokenException
)


def encode_jwt(
        payload: dict,
        expire_timedelta: int,  # minutes
        private_key: str = settings.AUTH_JWT_PRIVATE,
        algorithm: str = settings.AUTH_JWT_ALGORITHM
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    exp = now + timedelta(minutes=expire_timedelta)
    to_encode.update(exp=exp, iat=now)
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
        token: str,
        public_key: str = settings.AUTH_JWT_PUBLIC,
        algorithm: str = settings.AUTH_JWT_ALGORITHM
) -> dict:
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def create_access_jwt(
        payload: dict,
        expire_timedelta: int = settings.ACCESS_JWT_EXPIRE_MINUTES
) -> str:
    to_encode = payload.copy()
    to_encode.update(type='access')
    token = encode_jwt(to_encode, expire_timedelta)
    return token


async def create_refresh_jwt(
        payload: dict,
        expire_timedelta: int = settings.REFRESH_JWT_EXPIRE_MINUTES
) -> str:
    to_encode = payload.copy()
    to_encode.update(type='refresh')
    token = encode_jwt(to_encode, expire_timedelta)
    token_id = await RefreshJWTDAO.update_jwt(user_id=int(to_encode.get('sub')), new_token=token)
    if not token_id:
        raise FailedToCreateTokenException
    return token


async def create_tokens(payload: dict) -> tuple:
    access_token = create_access_jwt(payload)
    refresh_token = await create_refresh_jwt(payload)
    return access_token, refresh_token


async def validate_token(token: str):
    try:
        payload = decode_jwt(token)
    except (jwt.PyJWTError, AttributeError):
        raise InvalidTokenException

    user_id = int(payload.get('sub'))
    expire = payload.get('exp')
    token_type = payload.get('type')
    if not user_id or not expire or not token_type:
        raise InvalidTokenException

    if int(expire) < datetime.utcnow().timestamp():
        raise ExpiredTokenException

    if token_type not in ('access', 'refresh'):
        raise InvalidTokenException

    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserDoesNotExistException

    return payload


async def recreate_tokens(request: Request) -> tuple:
    """Recreate access and refresh tokens depends on refresh token:
    - If access token is validated then return current access and refresh tokens,
    - If access token is not validated then create new access and refresh tokens,
    - If access and refresh tokens is not validated then return InvalidTokenException"""

    access_token = request.cookies.get('access_token')
    refresh_token = request.cookies.get('refresh_token')

    try:
        await validate_token(access_token)
    except (jwt.PyJWTError, AttributeError, HTTPException):
        payload = await validate_token(refresh_token)

        user_id = int(payload.get('sub'))
        saved_token = await RefreshJWTDAO.find_one_or_none(user_id=user_id)
        if not saved_token or saved_token.token != refresh_token:
            raise InvalidTokenException
        access_token, refresh_token = await create_tokens(payload)

    return access_token, refresh_token
