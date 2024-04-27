import uuid
from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import jwt

from app.settings import settings


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


def create_registration_confirmation_code() -> str:
    return str(uuid.uuid4())
