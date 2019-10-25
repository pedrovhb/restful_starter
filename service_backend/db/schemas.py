from datetime import datetime, date
from typing import List

from pydantic import Schema, BaseModel, SecretStr, IPvAnyAddress, EmailStr


class UserSchema(BaseModel):
    name: str = Schema(..., min_length=2, max_length=255)
    email: EmailStr = Schema(...)
    registration_date: datetime = datetime.now()

    class Config:
        orm_mode = True


class UserRegisterSchema(UserSchema):
    password: SecretStr = Schema(..., min_length=6, max_length=255)


class UserDBSchema(UserRegisterSchema):
    registration_ip: str = None

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    email: EmailStr = Schema(...)
    password: SecretStr = Schema(...)
