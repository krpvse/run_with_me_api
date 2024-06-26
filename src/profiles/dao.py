from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.dao.base import BaseDAO
from src.database import scoped_session
from src.exceptions.error_handlers import dao_error_handler
from src.profiles.dto import CoordinatesDTO, ProfileInfoDTO
from src.profiles.models import Coordinates, Runners, Users


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    @dao_error_handler
    async def get_user_info(cls, user_id: int):
        async with scoped_session() as session:
            query = select(cls.model).where(cls.model.id == user_id).options(
                selectinload(cls.model.runner).selectinload(Runners.coordinates)
            )
            result = await session.execute(query)
            user = result.scalars().one_or_none()
            user_dto = ProfileInfoDTO.model_validate(user, from_attributes=True) if user else None
            return user_dto


class RunnersDAO(BaseDAO):
    model = Runners


class CoordinatesDAO(BaseDAO):
    model = Coordinates

    @classmethod
    @dao_error_handler
    async def get_coordinates(cls, **filter_by):
        async with scoped_session() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            coords = result.scalars()
            coords_dto = [CoordinatesDTO.model_validate(c, from_attributes=True) for c in coords if c]
            return coords_dto
