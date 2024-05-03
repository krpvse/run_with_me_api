from typing import Optional

from pydantic import BaseModel, model_validator


class SProfile(BaseModel):
    """
    Validate class:
    1. If client don't write value, this field will be deleted after validation;
    2. If client write null value for field, this value will save after validation
    """

    name: Optional[str] = None
    age: Optional[int] = None
    description: Optional[str] = None
    distance_from: Optional[int] = None
    distance_to: Optional[int] = None
    speed_from: Optional[int] = None
    speed_to: Optional[int] = None


    @model_validator(mode='before')
    @classmethod
    def check_all_none(cls, values):
        values = {k: v for k, v in values.items() if v}
        if not values:
            raise ValueError('No values')
        return values

    @model_validator(mode='before')
    @classmethod
    def check_wrong_undefined_keys(cls, values):
        for k in values:
            if k not in cls.model_fields:
                raise ValueError(f'Value {k} is not defined')
        return values

    @model_validator(mode='before')
    @classmethod
    def set_not_specified_fields(cls, values):
        cls.__not_specified = []
        for field in cls.model_fields:
            if field not in values.keys():
                cls.__not_specified.append(field)
        return values

    @model_validator(mode='after')
    def delete_not_specified_fields(self):
        for field in self:
            if field[0] in self.__not_specified:
                delattr(self, field[0])
        return self


class SCoords(BaseModel):
    latitude: float
    longitude: float
