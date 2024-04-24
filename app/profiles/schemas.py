from pydantic import BaseModel, model_validator


class SProfile(BaseModel):
    name: str = None
    age: int = None
    description: str = None
    distance_from: int = None
    distance_to: int = None
    speed_from: int = None
    speed_to: int = None

    class Config:
        fields = {
            'name': {'exclude': True},
            'age': {'exclude': True},
            'description': {'exclude': True},
            'distance_from': {'exclude': True},
            'distance_to': {'exclude': True},
            'speed_from': {'exclude': True},
            'speed_to': {'exclude': True},
        }

    @model_validator(mode='before')
    @classmethod
    def check_existing_values(cls, values):
        values = {k: v for k, v in values.items() if v}
        if not values:
            raise ValueError('No values')
        return values

    @model_validator(mode='before')
    @classmethod
    def check_undefined_values(cls, values):
        for k in values:
            if k not in cls.model_fields:
                raise ValueError(f'Value {k} is not defined')
        return values
