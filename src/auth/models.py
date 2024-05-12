from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.dao.types import int_pk
from src.database import Base


class RefreshJWT(Base):
    __tablename__ = 'refresh_jwts'

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    token: Mapped[str]
