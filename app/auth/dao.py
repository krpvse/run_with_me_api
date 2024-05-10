from sqlalchemy.dialects.postgresql import insert

from app.auth.models import RefreshJWT
from app.dao.base import BaseDAO
from app.database import scoped_session
from app.exceptions.error_handlers import dao_error_handler


class RefreshJWTDAO(BaseDAO):
    model = RefreshJWT

    @classmethod
    @dao_error_handler
    async def update_jwt(cls, user_id: int, new_token: str):
        async with scoped_session() as session:
            stmt = insert(cls.model).values(user_id=user_id, token=new_token)
            stmt = stmt.on_conflict_do_update(
                index_elements=[cls.model.user_id],
                set_=dict(token=stmt.excluded.token)
            ).returning(cls.model.id)

            result = await session.execute(stmt)
            row_id = result.scalar_one_or_none()
            await session.commit()
            return row_id
