from datetime import datetime
from jose import jwt, JWTError

from fastapi import Request

from app.settings import settings
from app.profiles.dao import UsersDAO
from app.exceptions import (UserDoesNotExistsException, TokenDoesNotExistsException, InvalidTokenException,
                            ExpiredTokenException, NoParamException)


class Dependencies:
    def __init__(self, request: Request):
        self.__request = request

    @property
    def path_params(self):
        return self.__request.path_params

    def get_access_token(self):
        access_token = self.__request.cookies.get('access_token')
        if not access_token:
            raise TokenDoesNotExistsException
        return access_token

    def get_profile_id(self):
        profile_id = self.path_params.get('profile_id')
        if not profile_id:
            raise NoParamException
        return int(profile_id) if profile_id else None

    async def get_current_user(self):
        try:
            payload = jwt.decode(self.get_access_token(), settings.SECRET_KEY, settings.HASH_ALGORITHM)
        except (JWTError, AttributeError):
            raise InvalidTokenException

        expire = payload.get('exp')
        if not expire or int(expire) < datetime.utcnow().timestamp():
            raise ExpiredTokenException

        user_id = payload.get('sub')
        if not user_id:
            raise InvalidTokenException

        user = await UsersDAO.find_one_or_none(id=int(user_id))
        if not user:
            raise UserDoesNotExistsException

        return user
