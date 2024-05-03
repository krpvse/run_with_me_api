from typing import Optional

from pydantic import BaseModel, EmailStr


class CoordinatesDTO(BaseModel):
    id: int
    latitude: float
    longitude: float


class RunnerDTO(BaseModel):
    name: str
    age: int | None
    description: str | None
    distance_from: int | None
    distance_to: int | None
    speed_from: int | None
    speed_to: int | None

    coordinates: Optional[list['CoordinatesDTO']]


class ProfileInfoDTO(BaseModel):
    id: int
    email: EmailStr

    runner: 'RunnerDTO'
