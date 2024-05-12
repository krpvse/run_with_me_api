import uuid

from passlib.context import CryptContext

from src.cache.cache import RegConfirmCodeCache


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


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
