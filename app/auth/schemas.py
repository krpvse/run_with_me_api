from string import digits, ascii_uppercase

from pydantic import BaseModel, EmailStr, field_validator, model_validator


class SUserAuth(BaseModel):
    email: EmailStr
    password1: str


class SJWTToken(BaseModel):
    token: str
    type: str = 'Bearer'


class SUserReg(SUserAuth):
    password2: str
    name: str

    @staticmethod
    def __check_on_length(v: str):
        return len(v) >= 8

    @staticmethod
    def __check_on_capital_letters(v: str):
        return bool(filter(lambda x: x in ascii_uppercase, v))

    @staticmethod
    def __check_on_digits(v: str):
        return bool(filter(lambda x: x in digits, v))

    @field_validator('password1')
    @classmethod
    def password_validator(cls, v: str):
        if not all([cls.__check_on_length(v), cls.__check_on_capital_letters(v), cls.__check_on_digits(v)]):
            raise ValueError('Wrong password. Check on constraints:\n'
                             '- Password length >= 8 chars,\n'
                             '- Should be 1 and more capital letters,\n'
                             '- Should be 1 and more digits\n')
        return v

    @model_validator(mode='before')
    @classmethod
    def passwords_equality(cls, values):
        if values.get('password2') and values.get('password1') != values.get('password2'):
            raise ValueError('Password mismatch')
        return values
