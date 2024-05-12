from typing import Literal

import pem
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    MODE: Literal['DEV', 'TEST', 'PROD']

    SECRET_KEY: str
    DOMAIN: str
    PASSWORD_HASH_ALGORITHM: str

    AUTH_JWT_ALGORITHM: str
    ACCESS_JWT_EXPIRE_MINUTES: int = 30
    REFRESH_JWT_EXPIRE_MINUTES: int = 43200  # 30 days

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
        return (f'postgresql+asyncpg://{cls.POSTGRES_USER}:{cls.POSTGRES_PASSWORD}'
                f'@{cls.POSTGRES_HOST}:{cls.POSTGRES_PORT}/{cls.POSTGRES_DB}')

    @property
    def TEST_DATABASE_URL(cls):
        return (f'postgresql+asyncpg://{cls.TEST_POSTGRES_USER}:{cls.TEST_POSTGRES_PASSWORD}'
                f'@{cls.TEST_POSTGRES_HOST}:{cls.TEST_POSTGRES_PORT}/{cls.TEST_POSTGRES_DB}')

    @property
    def REDIS_URL(cls):
        return f'redis://{cls.REDIS_HOST}:{cls.REDIS_PORT}'

    @property
    def DOMAIN_URL(cls):
        return f'https://{cls.DOMAIN}' if cls.MODE == 'PROD' else 'http://0.0.0.0:8000'

    @property
    def AUTH_JWT_PRIVATE(cls):
        certs = pem.parse_file('src/auth/certs/jwt-private.pem')
        key = str(certs[0])
        return key

    @property
    def AUTH_JWT_PUBLIC(cls):
        certs = pem.parse_file('src/auth/certs/jwt-public.pem')
        key = str(certs[0])
        return key


settings = Settings()
