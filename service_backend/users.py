from fastapi import HTTPException
from peewee import fn, DoesNotExist
from starlette.requests import Request

from schemas import *
from models import *
from utils import log

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

pw_hasher = PasswordHasher()


def register_user(user_in: UserRegisterSchema, request: Request) -> UserSchema:
    log.info(f'Attempting to register user:\n{user_in}')

    # Verificar se usuário com esse e-mail já existe
    if User.select().where(fn.Lower(User.email) == user_in.email.lower()).exists():
        log.info(f'409: User {user_in.email} already exists.')
        raise HTTPException(409, 'e-mail already exists')

    hashed_password = pw_hasher.hash(user_in.password.get_secret_value())

    user_created_db = User.create(
        registration_ip=request.client.host,
        password=hashed_password,
        **user_in.dict(exclude={'password'}))

    user_db_schema = UserDBSchema.from_orm(user_created_db)
    return UserSchema(**user_db_schema.dict())


def login_user(user_login: UserLoginSchema) -> UserSchema:
    log.info(f'User login: {user_login.email}')

    user_orm = User.select().where(fn.Lower(User.email) == user_login.email.lower()).first()
    if user_orm is None:
        raise HTTPException(404, 'user does not exist')
    user_db = UserDBSchema.from_orm(user_orm)

    try:
        pw_hasher.verify(user_db.password.get_secret_value(), user_login.password.get_secret_value())
    except VerifyMismatchError:
        raise HTTPException(403, 'wrong password')

    return UserSchema.from_orm(user_orm)
