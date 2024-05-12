import asyncio
from contextlib import asynccontextmanager

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.settings import settings


if settings.MODE == 'TEST':
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {'poolclass': NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}


engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def scoped_session():
    scoped_factory = async_scoped_session(
        session_maker,
        scopefunc=asyncio.current_task,
    )
    try:
        async with scoped_factory() as s:
            yield s
    finally:
        await scoped_factory.remove()


class Base(DeclarativeBase):
    pass
