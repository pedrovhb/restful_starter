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

# class VetSchema(UserSchema):
#     crmv_rj: str = Schema(...)
#     phone_is_whatsapp: bool = Schema(...)
#     specialty: str = Schema(...)
#     bio_text: str = Schema(...)
#
#     class Config:
#         orm_mode = True
#
#
# class VetRegisterSchema(VetSchema):
#     password: SecretStr = Schema(...)
#     registration_ip: IPvAnyAddress = ...
#     registration_date: datetime = ...
#
#
# class WalkerSchema(UserSchema):
#     phone_is_whatsapp: bool = Schema(...)
#     bio_text: str = Schema(...)
#
#     class Config:
#         orm_mode = True
#
#
# class WalkerRegisterSchema(WalkerSchema):
#     password: SecretStr = Schema(...)
#     registration_ip: IPvAnyAddress = ...
#     registration_date: datetime = ...

# class MedicalRecord(BaseModel):
#     ...
#
#
# class DiseaseModel(BaseModel):
#     name: str = Schema(...)
#     description: str = Schema(...)
#
#
# class PetModel(BaseModel):
#     pet_name: str = Schema(...)
#     species: str = Schema(...)
#     breed: str = None
#     birth_date: date = None
#     gender: str = None
#     medical_records: List[MedicalRecord] = []
#     previous_diseases: List[str]
