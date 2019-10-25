import re

import jwt
from fastapi import HTTPException
from peewee import fn
from starlette.requests import Request

from models import User
from schemas import UserSchema
from utils import JWT_SECRET


def get_current_user(request: Request) -> UserSchema:
    jwt_token = request.cookies.get('Authorization')

    # Apparently the testclient's cookies aren't detected, although they're in the header.
    # We just try to get them manually here if that's the case
    if not jwt_token:
        try:
            cookie_str = request.headers.get('cookie', '')
            jwt_token = next(re.finditer('Authorization=(Bearer .*?)(?:[; ]|$)', cookie_str)).group(1)
        except (StopIteration, AttributeError):
            pass

    if jwt_token is None:
        raise HTTPException(401, 'authentication required')

    jwt_token = jwt_token.split(' ')[-1]
    try:
        decoded = jwt.decode(jwt_token, key=JWT_SECRET, algorithms=['HS256'])
        email = decoded.get('email')
    except jwt.exceptions.DecodeError:
        raise HTTPException(401, 'invalid jwt token')

    user_orm = User.select().where(fn.Lower(User.email) == email).first()
    user = UserSchema.from_orm(user_orm)
    return user
