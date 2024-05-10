import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import UniqueConstraint

from app.dao.types import int_pk
from app.database import Base


class Coordinates(Base):
    __tablename__ = 'coordinates'

    id: Mapped[int_pk]
    runner_id: Mapped[int] = mapped_column(ForeignKey('runners.user_id'))
    latitude: Mapped[float]
    longitude: Mapped[float]

    __table_args__ = (UniqueConstraint('runner_id', 'latitude', 'longitude', name='uniq_runner_id_latitude_longitude'),)


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
