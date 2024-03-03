from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.services.types import int_pk


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int_pk]
    email: Mapped[str] = mapped_column(String(length=128), unique=True, nullable=False)
    hashed_password: Mapped[str]


class Runners(Base):
    __tablename__ = 'runners'

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    name: Mapped[str] = mapped_column(String(length=128), nullable=False)
    age: Mapped[int | None]
    description: Mapped[str | None] = mapped_column(String(length=256))
    distance_from: Mapped[int | None]
    distance_to: Mapped[int | None]
    speed_from: Mapped[int | None]
    speed_to: Mapped[int | None]


class PlaceTypes(Base):
    __tablename__ = 'place_types'

    id: Mapped[int_pk]
    runner_id: Mapped[int] = mapped_column(ForeignKey('runners.user_id'))
    park: Mapped[bool]
    street: Mapped[bool]
    sport_ground: Mapped[bool]
    gym: Mapped[bool]


class Coordinates(Base):
    __tablename__ = 'coordinates'

    id: Mapped[int_pk]
    runner_id: Mapped[int] = mapped_column(ForeignKey('runners.user_id'))
    latitude: Mapped[int]
    longitude: Mapped[int]
