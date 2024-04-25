from sqlalchemy import select, insert, update

from app.database import session_maker


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def add(cls, **data):
        async with session_maker() as session:
            stmt = insert(cls.model).values(**data).returning(cls.model.id)
            result = await session.execute(stmt)
            user_id = result.scalar_one_or_none()
            await session.commit()
            return user_id

    @classmethod
    async def update(cls, update_data: dict, **filter_by):
        async with session_maker() as session:
            stmt = update(cls.model).filter_by(**filter_by).values(**update_data)
            await session.execute(stmt)
            await session.commit()
