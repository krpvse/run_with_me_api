from pydantic import BaseModel


class SProfile(BaseModel):
    name: str | None = None
    age: int | None = None
    description: str | None = None
    distance_from: int | None = None
    distance_to: int | None = None
    speed_from: int | None = None
    speed_to: int | None = None
