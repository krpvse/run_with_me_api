from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import session_maker
from app.dao.base import BaseDAO
from app.profiles.models import Users, Runners
from app.profiles.dto import UserDTO


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def get_user_info(cls, user_id: int):
        async with session_maker() as session:
            query = select(cls.model).where(cls.model.id == user_id).options(
                selectinload(cls.model.runner).selectinload(Runners.coordinates)
            )
            result = await session.execute(query)
            user = result.scalars().one_or_none()
            user_dto = UserDTO.model_validate(user, from_attributes=True) if user else None
            return user_dto


class RunnersDAO(BaseDAO):
    model = Runners
