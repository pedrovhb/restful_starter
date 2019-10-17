from datetime import datetime, date
from typing import List

from pydantic import Schema, BaseModel, SecretStr, IPvAnyAddress


# todo - validação de campos

class UserSchema(BaseModel):
    name: str = Schema(...)
    cpf: str = Schema(...)
    rg: str = Schema(...)
    address: str = Schema(...)
    email: str = Schema(...)
    phone: str = Schema(...)
    registration_date: datetime = datetime.now()

    class Config:
        orm_mode = True


class UserRegisterSchema(UserSchema):
    password: SecretStr = Schema(...)


class UserDBSchema(UserRegisterSchema):
    registration_ip: IPvAnyAddress = None

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    email: str = Schema(...)
    password: SecretStr = Schema(...)
