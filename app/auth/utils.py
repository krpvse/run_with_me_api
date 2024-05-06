import uuid
from datetime import datetime, timedelta

import pem
import jwt
from passlib.context import CryptContext

from app.settings import settings
from app.cache.cache import RegConfirmCodeCache

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def read_key(file_path: str):
    certs = pem.parse_file(file_path)
    key = str(certs[0])
    return key


def encode_jwt(
        payload: dict,
        private_key: str = read_key(settings.AUTH_JWT_PRIVATE_PATH),
        algorithm: str = settings.AUTH_JWT_ALGORITHM,
        expire_timedelta: int = 30  # minutes
):
    to_encode = payload.copy()
    exp = datetime.utcnow() + timedelta(minutes=expire_timedelta)
    to_encode.update({'exp': exp})
    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
        token: str,
        public_key: str = read_key(settings.AUTH_JWT_PUBLIC_PATH),
        algorithm: str = settings.AUTH_JWT_ALGORITHM
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def get_password_hash(password: str) -> bytes:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def create_confirmation_code(api_url: str, user_id: int, to_cache: bool = True):
    code = str(uuid.uuid4())
    link = f'{api_url}{user_id}/{code}'
    if to_cache:
        await RegConfirmCodeCache(user_id=user_id, code=code, expire_time=600).save_code()
    return code, link
