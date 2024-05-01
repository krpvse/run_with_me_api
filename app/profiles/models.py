import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.dao.types import int_pk


class Coordinates(Base):
    __tablename__ = 'coordinates'

    id: Mapped[int_pk]
    runner_id: Mapped[int] = mapped_column(ForeignKey('runners.user_id'))
    latitude: Mapped[float]
    longitude: Mapped[float]


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int_pk]
    email: Mapped[str] = mapped_column(String(length=128), unique=True)
    confirmed_email: Mapped[bool] = mapped_column(default=False)
    hashed_password: Mapped[str]
    registration_date: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow())

    runner: Mapped['Runners'] = relationship()


class Runners(Base):
    __tablename__ = 'runners'

    id: Mapped[int_pk]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), unique=True)
    name: Mapped[str] = mapped_column(String(length=128))
    age: Mapped[int | None]
    description: Mapped[str | None] = mapped_column(String(length=256))
    distance_from: Mapped[int | None]
    distance_to: Mapped[int | None]
    speed_from: Mapped[int | None]
    speed_to: Mapped[int | None]

    coordinates: Mapped[list['Coordinates']] = relationship()
