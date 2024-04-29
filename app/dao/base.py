from sqlalchemy import select, insert, update

from app.database import session_maker
from app.exceptions.error_handlers import dao_error_handler


class BaseDAO:
    model = None

    @classmethod
    @dao_error_handler
    async def find_one_or_none(cls, **filter_by):
        async with session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    @dao_error_handler
    async def add(cls, **data):
        async with session_maker() as session:
            stmt = insert(cls.model).values(**data).returning(cls.model.id)
            result = await session.execute(stmt)
            row_id = result.scalar_one_or_none()
            await session.commit()
            return row_id

    @classmethod
    @dao_error_handler
    async def update(cls, update_data: dict, **filter_by):
        async with session_maker() as session:
            stmt = update(cls.model).filter_by(**filter_by).values(**update_data)
            await session.execute(stmt)
            await session.commit()
