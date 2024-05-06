from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    MODE: Literal['DEV', 'TEST', 'PROD']

    SECRET_KEY: str
    DOMAIN: str
    PASSWORD_HASH_ALGORITHM: str

    AUTH_JWT_PRIVATE_PATH: str = 'app/auth/certs/jwt-private.pem'
    AUTH_JWT_PUBLIC_PATH: str = 'app/auth/certs/jwt-public.pem'
    AUTH_JWT_ALGORITHM: str

    REDIS_HOST: str
    REDIS_PORT: int

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    TEST_POSTGRES_HOST: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_DB: str
    TEST_POSTGRES_PORT: int

    @property
    def DATABASE_URL(cls):
        return f'postgresql+asyncpg://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DB}'

    @property
    def TEST_DATABASE_URL(cls):
        return f'postgresql+asyncpg://{cls.TEST_POSTGRES_USER}:{cls.TEST_POSTGRES_PASSWORD}@{cls.TEST_POSTGRES_HOST}:{cls.TEST_POSTGRES_PORT}/{cls.TEST_POSTGRES_DB}'

    @property
    def REDIS_URL(cls):
        return f'redis://{cls.REDIS_HOST}:{cls.REDIS_PORT}'

    @property
    def DOMAIN_URL(cls):
        return f'https://{cls.DOMAIN}' if cls.MODE == 'PROD' else f'http://127.0.0.1:8000'


settings = Settings()
