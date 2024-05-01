import uuid
from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import jwt

from app.settings import settings
from app.cache.cache import RegConfirmCodeCache


class AccessToken:
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=30)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.HASH_ALGORITHM)
        return encoded_jwt


class RegConfirmationCode:
    def __init__(self, api_url: str, user_id: int):
        self.__api_url = api_url
        self.__user_id = user_id
        self.code = str(uuid.uuid4())

    @property
    def link(self) -> str:
        confirmation_url = f'{self.__api_url}{self.__user_id}/{self.code}'
        return confirmation_url


async def get_confirmation_code(api_url: str, user_id: int, to_cache: bool = True):
    confirmation = RegConfirmationCode(api_url, user_id)
    if to_cache:
        await RegConfirmCodeCache(user_id=user_id, code=confirmation.code, expire_time=600).save_code()
    return confirmation.code, confirmation.link
