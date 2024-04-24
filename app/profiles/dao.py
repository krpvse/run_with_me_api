from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from app.database import session_maker
from app.dao.base import BaseDAO
from app.profiles.models import Users, Runners
from app.profiles.dto import UserDTO
from app.profiles.schemas import SProfile


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def get_user_info(cls, user_id: int):
        async with (session_maker() as session):
            query = select(cls.model).where(cls.model.id == user_id).options(
                selectinload(cls.model.runner).selectinload(Runners.coordinates)
            )
            result = await session.execute(query)
            user = result.scalars().one_or_none()
            user_dto = UserDTO.model_validate(user, from_attributes=True) if user else None
            return user_dto


class RunnersDAO(BaseDAO):
    model = Runners

    @classmethod
    async def update_profile(cls, profile_id: int, update_data: SProfile):
        update_data = update_data.dict(exclude_none=True)
        if update_data:
            async with session_maker() as session:
                stmt = update(cls.model).where(cls.model.user_id == profile_id).values(**update_data)
                await session.execute(stmt)
                await session.commit()
